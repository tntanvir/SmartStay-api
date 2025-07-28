from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
# from datetime import timedelta


# Create your models here.

class CustomUser(AbstractUser):
    name = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile = models.URLField(max_length=700, blank=True, null=True)
    role = models.CharField(max_length=50, choices=[
        ('admin', 'Admin'),
        ('user', 'User'),
        ('hotel owner', 'Hotel Owner')
    ], default='user', blank=True, null=True)
    

class EmailOTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)