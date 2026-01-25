from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from .views import UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', ObtainAuthToken.as_view(), name='login'),
]