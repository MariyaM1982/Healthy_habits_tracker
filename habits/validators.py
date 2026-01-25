from django.core.exceptions import ValidationError

from .models import Habit

def validate_habit(habit):
    # 1. Нельзя одновременно указывать вознаграждение и связанную привычку
    if habit.reward and habit.related_habit:
        raise ValidationError("Нельзя одновременно указывать вознаграждение и связанную привычку.")

    # 2. Время выполнения не более 120 секунд
    if habit.duration > 120:
        raise ValidationError("Время выполнения не должно превышать 120 секунд.")

    # 3. Связанная привычка должна быть приятной
    if habit.related_habit and not habit.related_habit.is_pleasant:
        raise ValidationError("Связанная привычка должна быть приятной.")

    # 4. У приятной привычки не может быть вознаграждения или связанной привычки
    if habit.is_pleasant:
        if habit.reward:
            raise ValidationError("У приятной привычки не может быть вознаграждения.")
        if habit.related_habit:
            raise ValidationError("У приятной привычки не может быть связанной привычки.")

    # 5. Периодичность от 1 до 7 дней
    if habit.frequency < 1 or habit.frequency > 7:
        raise ValidationError("Периодичность должна быть от 1 до 7 дней.")