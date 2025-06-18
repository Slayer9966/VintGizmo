from django.db import models

class HomeBanner(models.Model):
    main_text=models.CharField( max_length=255)
    secondry_text=models.CharField(max_length=255)
    banner_image=models.ImageField(upload_to='banners')
    main_text_color=models.CharField(default="#ffff")
    button_background=models.CharField(default="#ffff")
    button_color=models.CharField(default="#ffff")
    button_text=models.CharField(default="Shop Now")

