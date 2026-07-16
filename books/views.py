from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Author, Book
from .serializers import BookSerializer, AuthorSerializer


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
