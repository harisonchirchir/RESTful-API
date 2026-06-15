from django.urls import path
from . views import BookListCreateAPIView, BookDetailAPIview, AuthorsListCreateAPIView

urlpatterns = [
    path('books/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailAPIview.as_view(), name='book-detail'),
    path('authors/', AuthorsListCreateAPIView.as_view(), name='author-list-create'),
]
