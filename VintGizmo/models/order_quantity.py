from django.db import models
from .models import CustomUser
from django.utils.crypto import get_random_string
from .address import Address
from .products import Product  # Import your Product model
from .variation import Variation
from .orderItem import OrderItem

class OrderQuantity(models.Model):
    order_item = models.ForeignKey('OrderItem', on_delete=models.CASCADE,null=True, related_name='quantities')
    stock_code=models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)

    