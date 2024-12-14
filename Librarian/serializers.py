from rest_framework import serializers
from School.models import User, LibraryHistory, FeesHistory,Student
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model





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
    