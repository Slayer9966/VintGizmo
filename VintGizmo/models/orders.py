from django.db import models
from .models import CustomUser
from django.utils.crypto import get_random_string
from .address import Address
from .products import Product  # Import your Product model
from .variation import Variation

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_STATUS_CHOICES=[
        ('pending','Pending'),
        ('completed','Completed')
    ]

    address = models.CharField()
    order_id = models.CharField(max_length=9, unique=True, blank=True)  # 9-digit unique ID
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)  # User who placed the order (optional)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Phone number (optional)
    email = models.EmailField()  # User's email
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Total cost of the order
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Shipping cost
    discounts = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Any applied discounts
    payment_method = models.CharField(max_length=50)  # Payment method used
   
    customer_name=models.CharField(default="NO Name")
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='pending')  # Order status
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the order was created

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id()
        super().save(*args, **kwargs)

    def generate_order_id(self):
        # Generate a unique 9-digit order ID
        while True:
            order_id = get_random_string(length=9, allowed_chars='0123456789')
            if not Order.objects.filter(order_id=order_id).exists():
                return order_id

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username if self.user else 'Guest'} - Status: {self.status}"
