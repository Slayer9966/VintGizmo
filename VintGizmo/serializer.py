# serializers.py
from rest_framework import serializers
from .models.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'username', 'Phone_Number', 'User_Profile_Pic', 'Unique_Password', 'Text_Password']
        extra_kwargs = {
            'password': {'write_only': True},
            'Unique_Password': {'write_only': True},
            'Text_Password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['username'],
            Phone_Number=validated_data['Phone_Number'],
            User_Profile_Pic=validated_data['User_Profile_Pic'],
            Text_Password=validated_data['password'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
class VerifyAccountSerializer(serializers.Serializer):
  email=serializers.EmailField()
  otp=serializers.CharField()
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)