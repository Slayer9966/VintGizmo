from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
import random
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from VintGizmo.models.models import CustomUser
from VintGizmo.email import send_otp_via_email
from VintGizmo.serializer import UserSerializer, VerifyAccountSerializer,LoginSerializer
from django.http import HttpResponse


# Functions
def my_view(request):
    response = HttpResponse("Your content here")
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response
def VerifyEmailPage(request):
    return render(request,'VerifyEmail.html')
def VerifyPage(request):
    email = request.session.get('email')
    ispassword=request.session.get('ispassword')
    if ispassword=="No":
        user=CustomUser.objects.filter(email=email).first()
        if(user.is_verified):
            messages.error(request, "User already Verified")
            return redirect('loginPage')
        send_otp_via_email(email)


    if not email:
        return redirect('register')
    return render(request, 'otp.html', {'email': email,'ispassword':ispassword})
def staff_Page(request):
    return render(request,'staff.html')
def admin_Page(request):
    return render(request,'admin.html')
def local_Page(request):
    return render(request,'local.html')
def Login_Page(request):
    return render(request,'signin.html')
def register_Page(request):
    return render(request,'signup.html')
def ForgotPasswordPage(request):
    return render(request,'ForgotPassword.html')
def NewPasswordPage(request):
    email=request.session.get('email')
    return render(request,'NewPassword.html',{'email':email})

User = get_user_model()

class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                if user.is_verified:
                    request.session['user_id'] = user.id
                    if user.is_superuser:
                        return HttpResponseRedirect('/AdminP/')
                    elif user.is_staff:
                        return HttpResponseRedirect('/staff/')
                    else:
                        return redirect('Home')
                else:
                     messages.error(request, "Your Account is not verified kindly verify your account.")
                     return redirect('/loginPage/')
            else:
                    messages.error(request, "Invalid email or password.")
                    return redirect('/loginPage/')        
        else:
             messages.error(request, "Something went wrong.Plz try later")
             return redirect('/loginPage/')   

# API VIEW
class RegisterAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                send_otp_via_email(serializer.data['email'])
                request.session['email'] = serializer.data['email']  # Save email in session
                return redirect('VerifyPage')  # Redirect to OTP verification page
            
            messages.error("Something Went wrong try again later")
            return redirect('registerPage')
        except Exception as e:
            messages.error("Something Went wrong try again later")
            return redirect('registerPage')
class VerifyOTP(APIView):
    def post(self, request):
        try:
            ispassword = request.data.get('ispassword')

            data = request.data

            serializer = VerifyAccountSerializer(data=data)
            
            if serializer.is_valid():
                email = serializer.validated_data['email']
                otp = serializer.validated_data['otp']
                user = CustomUser.objects.filter(email=email).first()
                

                
                if not user:
                   messages.error("Can't find the account kindly signUp first")
                   return redirect('loginPage')
                if user.otp != otp:
                    messages.error(request, "Wrong OTP")
                    return redirect('/VerifyPage/')
                if ispassword=="yes":
                    request.session['email']

                    return redirect('NewPasswordPage')

                user.is_verified = True
                user.save()
                
                messages.success(request, "Account Verified Successfully plz login to your account")
                return redirect('/loginPage/')
            
            messages.error("Something went wrong plz try again later")
            return HttpResponseRedirect(request.META['HTTP_REFERER'])

        
        except Exception as e:
             messages.error("Something went wrong plz try again later")
             return HttpResponseRedirect(request.META['HTTP_REFERER'])

def user_logout(request):
    auth_logout(request)  # Use Django's built-in logout function
    return redirect('Home')

def generate_otp():
    return random.randint(100000, 999999)
def resend_otp(request):
    email = request.session.get('email')
    if email:
        user = CustomUser.objects.filter(email=email).first()
       
        if user:
            send_otp_via_email(email)
            return JsonResponse({'status': 'success', 'message': 'OTP sent successfully'})
        return JsonResponse({'status': 'error', 'message': 'Invalid email'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Email not found in session'}, status=400)



def ForgotPassword(request):
    email=request.POST.get('email')
    ispassword=request.POST.get('ispassword')
    user = CustomUser.objects.filter(email=email).first()
   
    if user :
           
        
                send_otp_via_email(email)
                request.session['email']=email
                request.session['ispassword']=ispassword
                return  redirect('VerifyPage')
    else:
           messages.error(request, "Account not found")
           return redirect('ForgotPasswordPage')

def ChangePassword(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    user=User.objects.filter(email=email).first()
   
    user.set_password(password)
    user.Text_Password=password;
    user.save();
    messages.success(request,"Password Updated Successfully")
    return redirect('loginPage')
   