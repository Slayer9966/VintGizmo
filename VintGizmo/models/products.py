from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from .models import CustomUser
from .category import Category  # Update import path if needed
from .brand import Brand  # Update import path if needed

class Product(models.Model):
    user = models.ForeignKey(CustomUser, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
   
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
  
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipping_cost=models.IntegerField(default=0)

    def __str__(self):
        return self.name
