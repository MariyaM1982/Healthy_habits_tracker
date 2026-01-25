import os
from celery import Celery
from django.conf import settings

# Указываем Django-настройки
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habit_tracker.settings')

app = Celery('habit_tracker')

# Загружаем конфигурацию из Django-настроек с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находит задачи в приложениях
app.autodiscover_tasks()