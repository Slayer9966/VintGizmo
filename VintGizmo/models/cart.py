from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from .models import CustomUser
from .category import Category  # Update import path if needed
from .brand import Brand
from .products import Product
from .variation import Variation
class Cart(models.Model):
    customer = models.ForeignKey(CustomUser, related_name='cart_items', on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, related_name='owned_products', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} by {self.customer.username}"