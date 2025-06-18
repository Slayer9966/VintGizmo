from django.db import models
from .models import CustomUser
class Brand(models.Model):
    BrandName=models.CharField(max_length=128)
    BrandDescription=models.TextField()
    BrandImage=models.ImageField(upload_to="Brands")
    user=models.ForeignKey('CustomUser',on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.BrandName
