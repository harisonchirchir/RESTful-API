from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Book, Author


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'biography']


class BookSerializer(serializers.ModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        write_only=True
    )
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'is_read', 'owner', 'author_id', 'author']
        read_only_fields = ['owner']
