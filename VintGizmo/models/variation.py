from django.db import models
from .products import Product

class Variation(models.Model):
    product_id=models.ForeignKey(Product,related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    sales_price = models.DecimalField(max_digits=15, decimal_places=2)
    sale_price=models.DecimalField(max_digits=15,decimal_places=2)
    warranty = models.IntegerField()
    description = models.TextField()
    quantity= models.IntegerField(default=0)