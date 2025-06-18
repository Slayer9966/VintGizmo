from django.db import models
from .products import Product
from .variation import Variation
from .orders import Order
from django.utils import timezone

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    variation = models.ForeignKey('Variation', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price=models.DecimalField(default=0,max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
