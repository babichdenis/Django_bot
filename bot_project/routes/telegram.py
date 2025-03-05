from aiogram.filters import Command
from handlers.telegram_handlers import send_welcome

def setup_telegram_routes(dp):
    """Настройка Telegram-обработчиков."""
    dp.message.register(send_welcome, Command("start"))
