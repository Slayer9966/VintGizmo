from django.db import models
import random
import string
from datetime import date
from .products import Product
from .variation import Variation

class Stock(models.Model):
    variation_id = models.ForeignKey(Variation, on_delete=models.CASCADE, related_name='stocks')
    

    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total_quantity = models.PositiveIntegerField()
    code = models.CharField(max_length=9, unique=True, editable=False)
    date_of_store = models.DateField(default=date.today)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = ''.join(random.choices(string.digits, k=9))
        super(Stock, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.variation_id} - {self.code}"