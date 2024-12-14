import re
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils import timezone
import phonenumbers

# Phone number validator
phone_regex = RegexValidator(
    regex=r'^\d{9,15}$', 
    message="Phone number must be between 9 and 15 digits."
)

# Manager for User model
class UserManager(BaseUserManager):
    def create_user(self, email, password, role, full_name=None, phone_number=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, role=role, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, full_name=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, role='admin', full_name=full_name, **extra_fields)

# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):  # Inherit PermissionsMixin here
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('office_staff', 'Office Staff'),
        ('librarian', 'Librarian'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, validators=[phone_regex], null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='office_staff')
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    address = models.CharField(max_length=255)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.phone_number:
            full_number = f"{self.phone_number}"
            try:
                parsed_number = phonenumbers.parse(full_number, None)
                if phonenumbers.is_valid_number(parsed_number):
                    self.phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
                else:
                    raise ValueError("Invalid phone number format.")
            except phonenumbers.phonenumberutil.NumberParseException:
                raise ValueError("Invalid phone number format.")
        super().save(*args, **kwargs)



# Student model


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()  # Date of birth
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    roll_number = models.CharField(max_length=20, unique=True)
    class_name = models.CharField(max_length=50) 
    created_at = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# LibraryHistory

class LibraryHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=255)
    borrow_date = models.DateField()
    return_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('borrowed', 'Borrowed'), ('returned', 'Returned')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"library history of {self.student} "


# FeesHistory
class FeesHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"library history of {self.student} "



class LibraryReview(models.Model):

    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)  
    book = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES) 
    comment = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Review of '{self.book}' by {self.student.first_name} ({self.rating}/5)"