# habits/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, set_telegram_chat_id

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')


urlpatterns = [
    path('set_chat_id/', set_telegram_chat_id, name='set_chat_id'),
] + router.urls