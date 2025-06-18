from django.db import models

class homeImage(models.Model):
    image_text=models.CharField(max_length=50)
    image=models.ImageField(upload_to='store/homeImage')

