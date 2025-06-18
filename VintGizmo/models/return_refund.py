# from django.db import models
# from .models import CustomUser
# from django.utils import timezone
# from .orders import Order

# class ReturnRefund(models.Model):
#     RETURN_STATUS_CHOICES = [
#         ('Pending', 'pending'),
#         ('Approved', 'approved'),
#         ('Rejected', 'rejected'),
#         ('Processed', 'processed'),
#     ]

#     REFUND_STATUS_CHOICES = [
#         ('Initiated', 'initiated'),
#         ('Completed', 'completed'),
#         ('Failed', 'failed'),
#     ]

#     order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='returns')
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     reason = models.TextField()
#     return_requested_at = models.DateTimeField(default=timezone.now)
#     return_status = models.CharField(max_length=20, choices=RETURN_STATUS_CHOICES, default='Pending')
#     refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     refund_status = models.CharField(max_length=20, choices=REFUND_STATUS_CHOICES, null=True, blank=True)
#     refund_processed_at = models.DateTimeField(null=True, blank=True)
#     notes = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return f"Return/Refund for {self.order_item.product.name} by {self.user.username}"

