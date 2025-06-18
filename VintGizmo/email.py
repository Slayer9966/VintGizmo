from django.core.mail import send_mail
import random
from django.conf import settings
from .models.models import CustomUser

def send_otp_via_email(email):
    subject= f"Your account verification email"
    otp=random.randint(0,1000)
    email_from=settings.EMAIL_HOST
    message=f"Your otp is {otp}"
    send_mail(subject,message,email_from,[email])
    user_obj=CustomUser.objects.get(email=email)
    user_obj.otp=otp
    user_obj.save()
