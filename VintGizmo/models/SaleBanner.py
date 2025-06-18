from django.db import models

class SaleBanner(models.Model):
    title=models.CharField(max_length=255)
    second_text=models.CharField(max_length=255)
    paragraph=models.TextField()
    sale=models.IntegerField()
    image=models.ImageField(upload_to='store/banners')
    background=models.CharField(default="#ffff")
    main_text_color=models.CharField(default="#ffff")
    secondry_color=models.CharField(default="#ffff")
    button_background=models.CharField(default="#ffff")
    button_text=models.CharField(default="Shop Now")