from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')

app_name = 'core'

urlpatterns = [
    path('core/', include(router.urls)),
]