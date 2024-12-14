# serializers.py
from rest_framework import serializers
from .models import User, LibraryHistory, FeesHistory,Student
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'role', 'password', 'confirm_password']
    
    def validate(self, data):
        # Check if password and confirm_password match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        # Remove confirm_password field before creating user
        validated_data.pop('confirm_password')

        # Create the user using the validated data
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            full_name=validated_data['full_name'],
            
        )
        return user
    


#LOGIN SERIALIZER

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        # Authenticate based on email and password
        User = get_user_model()
        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        return {
            'user': user,
            'email': user.email,
            'full_name': user.full_name,
            'role': user.role
        }
    


# LibraryHistory Serializer

class LibraryHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryHistory
        fields = '__all__'  



# FeesHistory Serializer

class FeesHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeesHistory
        fields = '__all__'  


# student serializer

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'