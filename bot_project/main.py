# main.py
import asyncio
import logging
from pathlib import Path
from aiogram import Bot, Dispatcher
from aiohttp import web
import aiohttp_jinja2 as aioj
import jinja2
from decouple import config
from handlers.web_handlers import handle_index, handle_category
from database.db import database
from routes.web import setup_web_routes
from routes.telegram import setup_telegram_routes
from aiohttp_session import setup, get_session, SimpleCookieStorage


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Определение путей
BASE_DIR = Path(__file__).resolve().parent.parent  
MEDIA_DIR = BASE_DIR / "media" 
TEMPLATES_DIR = BASE_DIR / "bot_project" / "templates" 



async def main():
    try:
        logger.info("Starting bot initialization...")

        # Инициализация бота
        bot = Bot(token=config("BOT_TOKEN"))
        dp = Dispatcher()

        # Инициализация базы данных
        await database.connect() 
        # Инициализация веб-сервера
        app = web.Application()
        setup(app, SimpleCookieStorage())
        aioj.setup(app, loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)))

        # Маршруты
        setup_web_routes(app, str(MEDIA_DIR))
        setup_telegram_routes(dp)

        # Запуск веб-сервера
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, config("HOST", default="localhost"), config("PORT", default=8080, cast=int))
        await site.start()
        logger.info(f"Web server started at {config('HOST')}:{config('PORT')}")

        # Запуск бота
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    except Exception as e:
        logger.critical(f"Application failed: {e}", exc_info=True)
    finally:
        await database.pool.close()  
        await bot.session.close()
        logger.info("Bot stopped")

if __name__ == "__main__":
    asyncio.run(main())
