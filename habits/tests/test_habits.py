# habits/tests/test_models.py
import os
import django
import sys

# 1. Добавьте путь к проекту
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# 2. Установите переменную окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habit_tracker.settings')

# 3. ВАЖНО: вызовите django.setup() ДО импортов
django.setup()

# 4. Теперь импортируем pytest и модели
import pytest
from django.core.exceptions import ValidationError
from users.models import User
from habits.models import Habit


@pytest.mark.django_db
def test_duration_validation():
    user = User.objects.create_user(username='test', password='test')
    habit = Habit(user=user, place='дом', time='08:00', action='пить воду', duration=150)
    with pytest.raises(ValidationError):
        habit.full_clean()


@pytest.mark.django_db
def test_pleasant_habit_cannot_have_reward():
    user = User.objects.create_user(username='test', password='test')
    habit = Habit(user=user, place='дом', time='08:00', action='пить воду', is_pleasant=True, reward='шоколадка')
    with pytest.raises(ValidationError):
        habit.full_clean()


@pytest.mark.django_db
def test_related_habit_must_be_pleasant():
    user = User.objects.create_user(username='test', password='test')
    habit1 = Habit.objects.create(user=user, place='дом', time='08:00', action='бег', is_pleasant=False)
    habit2 = Habit(user=user, place='дом', time='08:00', action='отдых', related_habit=habit1)
    with pytest.raises(ValidationError):
        habit2.full_clean()


@pytest.mark.django_db
def test_cannot_have_reward_and_related_habit():
    user = User.objects.create_user(username='test', password='test')
    habit1 = Habit.objects.create(user=user, place='дом', time='08:00', action='бег', is_pleasant=True)
    habit = Habit(user=user, place='дом', time='08:00', action='пить воду', reward='сок', related_habit=habit1)
    with pytest.raises(ValidationError):
        habit.full_clean()


@pytest.mark.django_db
def test_frequency_must_be_1_to_7():
    user = User.objects.create_user(username='test', password='test')
    habit = Habit(user=user, place='дом', time='08:00', action='пить воду', frequency=8)
    with pytest.raises(ValidationError):
        habit.full_clean()