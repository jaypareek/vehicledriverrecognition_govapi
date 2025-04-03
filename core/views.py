# views.py
from rest_framework import viewsets
from datetime import datetime, timedelta
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Profiles
from .serializers import ProfileSerializer
from random import SystemRandom
import json
import requests


def generate_otp():
    # Using SystemRandom() which is cryptographically secure
    secure_random = SystemRandom()
    # Generate a random number between 1000 and 9999
    otp = secure_random.randint(1000, 9999)
    return otp



class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profiles.objects.all()
    serializer_class = ProfileSerializer

    @action(detail=False, methods=['get'])
    def by_phone(self, request):
        phone_number = request.query_params.get('phone', None)
        
        if not phone_number:
            return Response(
                {'error': 'Phone number is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if not phone_number.isdigit() or len(phone_number) != 10:
            return Response(
                {'error': 'Invalid phone number format. Must be 10 digits.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            profile = self.queryset.get(mob=phone_number)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except Profiles.DoesNotExist:
            return Response(
                {'error': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def by_aadhar(self, request):
        aadhar = request.query_params.get('aadhar', None)
        
        if not aadhar:
            return Response(
                {'error': 'Aadhar number is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if not aadhar.isdigit() or len(aadhar) != 12:
            return Response(
                {'error': 'Invalid Aadhar number format. Must be 12 digits.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            profile = self.queryset.get(aadhar=aadhar)
            serializer = self.get_serializer(profile)
            try: 
                otp = generate_otp()
                url = "http://localhost:8001/api/verification/"
                expiry_time = datetime.now() + timedelta(minutes=2)
                payload = {
                            "user_aadhar": str(aadhar),
                            "verification_code": str(otp),
                            "expiry_date": expiry_time.isoformat(),
                            "is_active": True
                        }
                headers = {
                    'Content-Type': 'application/json',
                }
                response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
                if response.status_code != 201:
                    return Response(
                        {'error': 'Failed to Create OTP'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            except:
                raise

            return Response(serializer.data)
        except Profiles.DoesNotExist:
            
            return Response(
                {'error': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
