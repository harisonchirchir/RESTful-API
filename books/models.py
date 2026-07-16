from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=200, unique=True)
    biography = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.name

    
class Book(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='books'
    )
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        related_name='books'
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'title']
        indexes = [
            models.Index(fields=['owner', 'is_read']),
        ]
        verbose_name_plural = 'Books'

    def __str__(self):
        author_name = self.author.name if self.author else "Unknown Author"
        return f"{self.title} by {author_name}"
