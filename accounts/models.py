import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    admin_role = 'admin'
    staff_role = 'staff'
    user_role = 'user'
    email = models.EmailField(unique=True)
    ROLE_CHOICES = [
        ("admin", 'Admin'),
        ("staff", 'Staff'),
        ("user", 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)



def __str__(self):
        return self.user.username

