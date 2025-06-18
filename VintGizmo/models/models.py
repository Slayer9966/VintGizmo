from django.contrib.auth.models import AbstractUser
from django.db import models
from ..manager import UserManager

class CustomUser(AbstractUser):
    Phone_Number = models.CharField(null=True, max_length=11)
    User_Profile_Pic = models.ImageField(null=True,upload_to="Profiles")
    Unique_Password = models.CharField(null=True,max_length=128)
    Text_Password = models.CharField(null=True,max_length=128)
    email = models.EmailField(max_length=128, unique=True)
    USERNAME_FIELD = 'email'
    is_verified = models.BooleanField(default=False)  # corrected typo
    otp = models.CharField(max_length=200, null=True, blank=True)

    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email
