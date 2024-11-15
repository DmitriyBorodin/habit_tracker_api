from habit.services import send_telegram_message
from celery import shared_task
from habit.models import Habit
from datetime import datetime, timedelta


@shared_task
def send_message_about_habit():
    now = datetime.now()
    current_weekday = now.isoweekday()
    print(current_weekday)
    habits = Habit.objects.filter(weekdays__number=current_weekday)

    for habit in habits:
        print(habit)
        habit_time = habit.time
        habit_datetime = datetime.combine(datetime.today(), habit_time)

        if habit_datetime - timedelta(minutes=5) <= now <= habit_datetime:
            tg_chat_id = habit.owner.tg_chat_id
            message = f"Я буду {habit.action} в это время: {habit.time} в этом месте: {habit.location}"
            try:
                send_telegram_message(chat_id=tg_chat_id, message=message)
            except Exception as e:
                print(f"Ошибка отправки сообщения в Telegram: {e}")
