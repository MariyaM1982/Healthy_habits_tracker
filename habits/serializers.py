from rest_framework import serializers
from .models import Habit

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        # Создаём временный экземпляр для валидации
        instance = Habit(**data)
        instance.user = self.context['request'].user
        instance.clean()  # вызывает clean() → validate_habit
        return data