# handlers/telegram_handlers.py
from aiogram import Bot, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.db import database
from utils.logger import logger
from decouple import config
from datetime import datetime
from database.queries import create_telegram_user

WEBAPP_URL = config("WEBAPP_URL")
CHANNEL_USERNAME = config("CHANNEL_USERNAME")

async def check_subscription(bot: Bot, user_id: int) -> bool:
    """Проверяет, подписан ли пользователь на канал."""
    try:
        chat_member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return chat_member.status not in ["left", "kicked", "restricted", "banned"]
    except Exception as e:
        logger.error(f"Ошибка при проверке подписки: {e}", exc_info=True)
        return False

async def send_welcome(message: types.Message, bot: Bot):
    """Обработчик команды /start."""
    try:
        user = message.from_user

        if not await check_subscription(bot, user.id):
            # Предлагаем подписаться на канал
            builder = InlineKeyboardBuilder()
            builder.row(types.InlineKeyboardButton(
                text="Подписаться на канал",
                url=f"https://t.me/{CHANNEL_USERNAME[1:]}"
            ))
            await message.answer(
                "Для использования бота, пожалуйста, подпишитесь на наш канал:",
                reply_markup=builder.as_markup()
            )
            return

        now = datetime.now()

        await create_telegram_user(user.id, user.username, user.first_name, user.last_name, now, now, True)
        web_app_url = WEBAPP_URL
        builder = InlineKeyboardBuilder()
        builder.row(
            types.InlineKeyboardButton(
                text="Открыть магазин 🛍",
                web_app=types.WebAppInfo(url=web_app_url)
            )
        )

        await message.answer(
            f"Привет, {user.first_name}!\n\n"
            "Добро пожаловать в наш магазин. Нажми кнопку ниже, "
            "чтобы начать покупки:",
            reply_markup=builder.as_markup()
        )
    except Exception as e:
        logger.error(f"Ошибка в send_welcome: {e}", exc_info=True)
        await message.answer("⚠️ Произошла ошибка. Попробуйте позже.")

async def show_help(message: types.Message):
    """Обработчик команды /help."""
    help_text = (
        "🛍 Доступные команды:\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать справку\n"
    )
    await message.answer(help_text)
