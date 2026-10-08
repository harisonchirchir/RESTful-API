from django.urls import path
from .views import (
    BookListCreateAPIView,
    BookDetailAPIView,
    AuthorsListCreateAPIView,
    RegisterAPIView,
    LoginAPIView,
)

urlpatterns = [
    path('books/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('authors/', AuthorsListCreateAPIView.as_view(), name='author-list-create'),
    path('register/', RegisterAPIView.as_view(), name='user-register'),
    path('login/', LoginAPIView.as_view(), name='user-login'),
]
