from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'biography')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'is_read', 'owner')
    list_filter = ('is_read',)
    search_fields = ('title',)
