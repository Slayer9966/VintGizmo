from django.db import models
from .models import CustomUser

class Category(models.Model):
    name=models.CharField(max_length=128)
    Description=models.TextField()
    Cat_Image=models.ImageField(upload_to="Category")
    user=models.ForeignKey('CustomUser',on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.name