# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models.models import CustomUser
admin.site.register(CustomUser)