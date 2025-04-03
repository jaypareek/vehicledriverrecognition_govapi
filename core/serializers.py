from rest_framework import serializers
from .models import Profiles

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        fields = [
            'id', 
            'full_name',
            'email',
            'mob',
            'aadhar',
            'driving_license',
            'driving_licence_type',
            'driving_licence_expiry',
            'profile_pic'
        ]
