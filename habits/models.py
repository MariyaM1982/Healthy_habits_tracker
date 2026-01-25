from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=100, verbose_name='Место')
    time = models.TimeField(verbose_name='Время выполнения')
    action = models.CharField(max_length=200, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Приятная привычка')
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Связанная привычка'
    )
    frequency = models.PositiveIntegerField(default=1, verbose_name='Периодичность (в днях)')
    reward = models.CharField(max_length=200, blank=True, verbose_name='Вознаграждение')
    duration = models.PositiveIntegerField(verbose_name='Время на выполнение (сек)', default=60)
    is_public = models.BooleanField(default=False, verbose_name='Публичная')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from .validators import validate_habit
        validate_habit(self)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}: {self.action}"