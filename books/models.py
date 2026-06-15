from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=200)
    biography = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    title = models.CharField(max_length= 200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='books')
    is_read = models.BooleanField(default=False)
    
    
    
    def __str__(self):
        owner_name = self.owner.username if self.owner else "No Owner"
        author_name = self.author.name if self.author else "No Author"
        return f"{self.title} (by {owner_name})"
