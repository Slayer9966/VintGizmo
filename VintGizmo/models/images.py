from django.db import models
from .products import Product
from .variation import Variation

class Images(models.Model):
    product = models.ForeignKey(Variation, related_name='images', on_delete=models.CASCADE)
    image=models.ImageField(upload_to="Products")
    def __str__(self):
        return self.name