# serializers.py
from rest_framework import serializers
from School.models import User, LibraryHistory, FeesHistory,Student, LibraryReview
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError






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


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)  
    role = serializers.ChoiceField(choices=['admin', 'office_staff', 'librarian'], required=True) 

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'phone_number', 'role', 'password']  

    def validate_role(self, value):
        if value not in ['admin', 'office_staff', 'librarian']:
            raise serializers.ValidationError("Invalid role. Only 'admin', 'office_staff', and 'librarian' are allowed.")
        return value

    def create(self, validated_data):
        """ Override create method to handle password hashing """
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)  # Hash the password before saving
        user.save()
        return user
    

class LibraryReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryReview
        fields = ['id', 'student', 'book', 'rating', 'comment', 'created_at']