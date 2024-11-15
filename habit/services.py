from config import settings
import requests


def send_telegram_message(chat_id, message):
    """Отправляет сообщения пользователям в Telegram"""
    params = {
        "text": message,
        "chat_id": chat_id,
    }
    requests.get(
        f"{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage", params=params
    )
