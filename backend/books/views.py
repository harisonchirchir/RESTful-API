from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import Author, Book
from .serializers import BookSerializer, AuthorSerializer, UserSerializer


class AuthorsListCreateAPIView(APIView):
    """
    List all authors or create a new author.
    GET: Returns paginated list of all authors.
    POST: Creates a new author.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookListCreateAPIView(APIView):
    """
    List user's books or create a new book.
    GET: Returns books for authenticated user. Supports filtering by is_read parameter.
    POST: Creates a new book for authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Book.objects.filter(owner=request.user)

        is_read_param = request.query_params.get('is_read', None)

        if is_read_param is not None:
            is_read_bool = is_read_param.lower() == 'true'
            queryset = queryset.filter(is_read=is_read_bool)

        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailAPIView(APIView):
    """
    Retrieve, update, or delete a specific book.
    GET: Returns book details for authenticated user.
    PUT: Updates book for authenticated user.
    DELETE: Deletes book for authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk, owner=request.user)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        book = get_object_or_404(Book, pk=pk, owner=request.user)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = get_object_or_404(Book, pk=pk, owner=request.user)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterAPIView(APIView):
    """
    Register a new user and return an authentication token.
    No authentication required.
    """
    permission_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {'token': token.key, 'username': user.username},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """
    Authenticate an existing user and return their token.
    No authentication required.
    """
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {'detail': 'Invalid username or password.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username})
