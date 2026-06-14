from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'is_read', 'owner']
        
        read_only_fields = ['owner']
