from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profiles(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    mob = models.CharField(max_length=10, unique=True)
    aadhar = models.CharField(max_length=12, unique=True)
    driving_license = models.CharField(max_length=16, unique=True)
    driving_licence_type = models.CharField(max_length=10)
    driving_licence_expiry = models.DateField()
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by')

    def __str__(self):
        return self.full_name