from datetime import time, datetime
from celery import shared_task
import requests
from django.conf import settings
from .models import Habit

@shared_task
def send_telegram_reminder(habit_id):
    """
    Отправляет напоминание о привычке в Telegram.
    """
    try:
        habit = Habit.objects.get(id=habit_id)
        chat_id = habit.user.telegram_chat_id
        if not chat_id:
            return  # У пользователя не указан chat_id

        message = (
            f"🔔 *Напоминание!* \n\n"
            f"Пора выполнить привычку:\n"
            f"*{habit.action}*\n"
            f"📍 Место: {habit.place}\n"
            f"⏰ Время: {habit.time.strftime('%H:%M')}\n"
        )
        if habit.reward:
            message += f"🎁 Вознаграждение: {habit.reward}"
        elif habit.related_habit:
            message += f"🎁 После этого — приятная привычка: {habit.related_habit.action}"

        # URL для отправки сообщения
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }

        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Ошибка отправки в Telegram: {response.text}")

    except Habit.DoesNotExist:
        print(f"Habit with id {habit_id} does not exist.")
    except Exception as e:
        print(f"Ошибка при отправке напоминания: {e}")

def check_habits_and_send_reminders():
    """
    Проверяет, у кого сейчас время привычки (с учётом дня недели и частоты).
    Отправляет напоминание через Telegram.
    """
    now = datetime.now(pytz.timezone('Europe/Moscow'))
    current_time = now.time()
    current_weekday = now.weekday()  # 0 = понедельник, 6 = воскресенье

    # Найдём все привычки
    habits = Habit.objects.select_related('user').all()

    for habit in habits:
        # Проверяем, совпадает ли время
        if not _is_time_to_execute(habit.time, current_time):
            continue

        # Проверяем, совпадает ли день (с учётом частоты)
        if not _is_day_to_execute(habit.frequency, current_weekday):
            continue

        # Отправляем напоминание
        send_telegram_reminder.delay(habit.id)

def _is_time_to_execute(habit_time: time, current_time: time, tolerance_seconds: int = 60) -> bool:
    """Проверяет, попадает ли текущее время в диапазон привычки ± tolerance."""
    habit_timedelta = datetime.combine(datetime.today(), habit_time)
    current_timedelta = datetime.combine(datetime.today(), current_time)
    diff = abs((habit_timedelta - current_timedelta).total_seconds())
    return diff <= tolerance_seconds

def _is_day_to_execute(frequency: int, current_weekday: int) -> bool:
    """
    Проверяет, должен ли пользователь выполнять привычку сегодня.
    Например: частота 1 — каждый день, 7 — раз в неделю (в тот же день).
    """
    if frequency == 1:
        return True  # каждый день
    # Для простоты: если частота > 1, проверяем, делится ли разница дней
    # Это упрощённая логика — в продакшене можно хранить last_completed
    return (current_weekday % frequency) == 0