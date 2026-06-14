from django.urls import path
from . views import BookListCreateAPIView, BookDetailAPIview

urlpatterns = [
    path('books/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailAPIview.as_view(), name='book-detail'),
]
