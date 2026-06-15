from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book, Author

class BookAPITestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='desmond', password='2108abcd')
        self.author = Author.objects.create(name='J.R.R. Tolkien', bio='English writer, poet, philologist, and academic.')
        self.url = reverse('book-list-create')

    def test_get_books_unauthorized_return_401(self):
        """Ensure unauthorized requests are blocked with a 401 status code."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_books_authenticated_return_200(self):
        """Ensure logged in users can access the book list and receive a 200 status code."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book_authenticated_returns_201(self):
        """Ensure logged in users can create a book and receive a 201 status code."""
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "The Silmarillion", 
            "author": self.author.id, 
            "is_read": False
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_filter_books_by_read_status(self):
        """Ensure users can filter books by their read status."""
        self.client.force_authenticate(user=self.user)
    
        Book.objects.create(title="Read Book", author=self.author, is_read=True, owner=self.user)
        Book.objects.create(title="Unread Book", author=self.author, is_read=False, owner=self.user)

        response = self.client.get(self.url, {'is_read': 'true'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Read Book")
