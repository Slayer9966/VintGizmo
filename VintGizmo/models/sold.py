from django.db import models
from .orders import Order
from .variation import Variation
from .models import CustomUser
from .orderItem import OrderItem

class SoldProduct(models.Model):
    order_item = models.ForeignKey('OrderItem',null=True, on_delete=models.CASCADE, related_name='sold_products')
    product_owner_id = models.ForeignKey('CustomUser',on_delete=models.CASCADE)
    variation = models.ForeignKey('Variation', on_delete=models.CASCADE, related_name='sold_products')
    sales_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.order.id} - Variation {self.variation.id} - Quantity {self.total_quantity}"
