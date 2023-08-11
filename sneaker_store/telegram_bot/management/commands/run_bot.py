from django.core.management.base import BaseCommand
from telegram_bot.bot import run_bot  # Импортируйте функцию для запуска вашего бота


class Command(BaseCommand):
    help = 'Run telegram bot'

    def handle(self, *args, **kwargs):
        run_bot()  # Запустите вашего бота