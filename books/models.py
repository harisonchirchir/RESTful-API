from django.db import models
from django.contrib.auth.models import User
class Book(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    title = models.CharField(max_length= 200)
    author = models.CharField(max_length= 200)
    is_read = models.BooleanField(default=False)
    
    
    
    def __str__(self):
        owner_name = self.owner.username if self.owner else "No Owner"
        return f"{self.title} (by {owner_name})"
