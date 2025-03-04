from aiohttp import web
import aiohttp_jinja2 as aioj
from aiogram import types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from database import get_categories, get_products_by_category, get_featured_products, pool
from logger import logger
from utils import handle_error

async def handle_index(request):
    try:
        featured_products = await get_featured_products()
        categories = await get_categories()
        context = {
            "featured_products": featured_products,
            "categories": categories,
        }
        return aioj.render_template("index.html", request, context)
    except Exception as e:
        return await handle_error(f"Error in handle_index: {e}")

async def handle_category(request):
    try:
        category_id = int(request.match_info["category_id"])
        products = await get_products_by_category(category_id)
        context = {
            "category_name": f"Категория {category_id}",
            "products": products,
        }
        return aioj.render_template("category.html", request, context)
    except Exception as e:
        return await handle_error(f"Error in handle_category: {e}")

async def send_welcome(message: types.Message):
    try:
        web_app_info = WebAppInfo(url="https://95e9-45-12-134-232.ngrok-free.app")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Открыть Web App", web_app=web_app_info)]
        ])
        await message.answer(
            "Привет! Нажми кнопку, чтобы открыть Web App:",
            reply_markup=keyboard,
        )
    except Exception as e:
        logger.error(f"Error in send_welcome: {e}")

async def handle_search(request):
    query = request.query.get("q", "").strip()
    if not query:
        return web.HTTPFound("/")  # Перенаправляем на главную, если запрос пустой

    async with pool.acquire() as conn:
        try:
            products = await conn.fetch(
                """SELECT id, name, price, main_image as image
                   FROM products_product
                   WHERE name ILIKE $1""",
                f"%{query}%"
            )
            context = {"products": products, "query": query}
            return aioj.render_template("search.html", request, context)
        except Exception as e:
            return await handle_error(f"Error in handle_search: {e}")
