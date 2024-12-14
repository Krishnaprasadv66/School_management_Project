# Generated by Django 5.1.4 on 2024-12-14 05:23

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('roll_number', models.CharField(max_length=20, unique=True)),
                ('class_name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be between 9 and 15 digits.', regex='^\\d{9,15}$')])),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('office_staff', 'Office Staff'), ('librarian', 'Librarian')], default='office_staff', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('address', models.CharField(max_length=255)),
                ('district', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pin_code', models.CharField(max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LibraryHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=255)),
                ('borrow_date', models.DateField()),
                ('return_date', models.DateField()),
                ('status', models.CharField(choices=[('borrowed', 'Borrowed'), ('returned', 'Returned')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='School.student')),
            ],
        ),
        migrations.CreateModel(
            name='FeesHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee_type', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateField()),
                ('remarks', models.TextField(blank=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='School.student')),
            ],
        ),
    ]
