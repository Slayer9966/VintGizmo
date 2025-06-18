from django.db import models

class StoreReview(models.Model):
    name=models.CharField(max_length=100)
    profession=models.CharField(max_length=50,null=True,default="user")
    image=models.ImageField(upload_to='StoreReview', null=True)
    review=models.TextField()
    status=models.CharField(default="pending",max_length=50)