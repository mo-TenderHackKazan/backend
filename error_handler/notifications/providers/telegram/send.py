import telebot
from django.conf import settings

from error_handler.notifications.models import Notification

if not settings.TELEGRAM_API_TOKEN:
    raise ValueError("please provide TELEGRAM_API_TOKEN env")
API_TOKEN = settings.TELEGRAM_API_TOKEN

bot = telebot.TeleBot(API_TOKEN)


def send_notification(notification: Notification) -> bool:
    if not notification.meta or "id" not in notification.meta:
        raise KeyError(f"can't send notification {notification.id}, id is not found")
    bot.send_message(
        notification.meta["id"],
        f"Новое уведомление на сайте\n{notification.title}\n{notification.body}",
    )

    return True
