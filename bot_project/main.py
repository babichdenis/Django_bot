import asyncio
import logging
from pathlib import Path
from aiogram import Bot, Dispatcher
from aiogram.filters import Command 
from aiohttp import web
import aiohttp_jinja2 as aioj
import jinja2
from handlers import handle_index, handle_category, send_welcome
from database import create_pool

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Определение путей
BASE_DIR = Path(__file__).resolve().parent.parent  # Корень проекта (my_project)
MEDIA_DIR = BASE_DIR / "media"  # Путь к внешней папке media
TEMPLATES_DIR = BASE_DIR / "bot_project" / "templates"  # Папка с шаблонами

# Проверка существования папок
if not MEDIA_DIR.exists():
    logger.error(f"Media directory not found: {MEDIA_DIR}")
    raise RuntimeError("Media directory is missing")

if not TEMPLATES_DIR.exists():
    logger.error(f"Templates directory not found: {TEMPLATES_DIR}")
    raise RuntimeError("Templates directory is missing")

async def main():
    try:
        logger.info("Starting bot initialization...")

        # Инициализация бота
        bot = Bot(token="7737966408:AAFxlaLbkFZpfpGTQz3VOzhaqkO7DOJuVzE")
        dp = Dispatcher()

        # Создание пула подключений к базе данных
        await create_pool()

        # Инициализация веб-сервера
        app = web.Application()
        aioj.setup(app, loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)))

        # Маршруты
        app.add_routes([
            web.get("/", handle_index),
            web.get("/category/{category_id}", handle_category),
            web.static("/media", str(MEDIA_DIR)),  # Доступ к медиафайлам
        ])

        # Регистрация обработчиков команд
        dp.message.register(send_welcome, Command(commands=["start"]))

        # Запуск веб-сервера
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "localhost", 8080)
        await site.start()
        logger.info("Web server started at http://localhost:8080")

        # Запуск бота
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    except Exception as e:
        logger.critical(f"Application failed: {e}", exc_info=True)
    finally:
        await bot.session.close()
        logger.info("Bot stopped")

if __name__ == "__main__":
    asyncio.run(main())
