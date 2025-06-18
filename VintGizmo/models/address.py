from django.db import models
from .models import CustomUser

class Address(models.Model):
    ADDRESS_TYPE_CHOICES = (
        ('billing', 'Billing'),
        ('shipping', 'Shipping'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=255, verbose_name="Full Name")
    phone_number = models.CharField(max_length=20, verbose_name="Phone Number")
    street_address=models.CharField(max_length=20,default='no')
    city = models.CharField(max_length=100, verbose_name="City")
    state = models.CharField(max_length=100, verbose_name="State/Region")
    postal_code = models.CharField(max_length=20, verbose_name="Postal Code")
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES, verbose_name="Address Type")
    is_default = models.BooleanField(default=False, verbose_name="Default Address")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.address_type.capitalize()} Address of {self.user}"

    def save(self, *args, **kwargs):
        # Ensure only one default address per user
        if self.is_default:
            Address.objects.filter(user=self.user, address_type=self.address_type).update(is_default=False)
        super(Address, self).save(*args, **kwargs)