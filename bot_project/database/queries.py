# database/queries.py
from database.db import database
from utils.logger import logger
from datetime import datetime


async def get_categories():
    """Получить все доступные категории."""
    query = "SELECT id, name, image FROM products_category"
    return await database.fetch_all(query)

async def get_category(category_id: int):
    """Получить категорию по ID."""
    query = "SELECT id, name, description, parent_id FROM products_category WHERE id = $1"
    return await database.fetch_one(query, category_id)

async def get_products_by_category(category_id: int, page: int = 1, per_page: int = 20):
    """Получить товары категории с пагинацией."""
    offset = (page - 1) * per_page
    query = """
        SELECT p.id, p.name, p.price, p.description, p.main_image as image
        FROM products_product p
        JOIN products_product_categories pc ON p.id = pc.product_id
        WHERE pc.category_id = $1 AND p.available = TRUE
        LIMIT $2 OFFSET $3
    """
    return await database.fetch_all(query, category_id, per_page, offset)

async def get_total_products_by_category(category_id: int):
    """Получить общее количество товаров в категории."""
    query = """
        SELECT COUNT(p.id)
        FROM products_product p
        JOIN products_product_categories pc ON p.id = pc.product_id
        WHERE pc.category_id = $1 AND p.available = TRUE
    """
    total_products = await database.fetchval(query, category_id)
    return total_products or 0 

async def get_product(product_id: int):
    """Получить полную информацию о товаре."""
    query = """
        SELECT id, name, price, description, 
               main_image as image, available
        FROM products_product
        WHERE id = $1 AND available = TRUE
    """
    return await database.fetch_one(query, product_id)

async def get_featured_products(limit=5):
    """Получить популярные товары."""
    query = """
        SELECT id, name, price, main_image as image
        FROM products_product
        WHERE available = TRUE
        ORDER BY created_at DESC
        LIMIT $1
    """
    return await database.fetch_all(query, limit)

async def product_exists(product_id: int) -> bool:
    """Проверить существование товара."""
    query = "SELECT EXISTS(SELECT 1 FROM products_product WHERE id = $1)"
    return await database.fetchval(query, product_id)

async def create_telegram_user(telegram_id: int, username: str, first_name: str, last_name: str, created_at:datetime, updated_at:datetime, is_active:bool):
    """Создает нового пользователя Telegram или обновляет существующего."""
    query = """
        INSERT INTO core_telegramuser (telegram_id, username, first_name, last_name, created_at, updated_at, is_active)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        ON CONFLICT (telegram_id) DO UPDATE SET
            username = $2,
            first_name = $3,
            last_name = $4,
            updated_at = $6
    """
    await database.execute(query, telegram_id, username, first_name, last_name, created_at, updated_at, is_active)


async def get_top_level_categories():
    """Получить категории первого уровня."""
    query = "SELECT id, name, image FROM products_category WHERE parent_id IS NULL"
    return await database.fetch_all(query)


async def get_subcategories(parent_id: int):
    """Получить вложенные категории по parent_id."""
    query = "SELECT id, name, image FROM products_category WHERE parent_id = $1"
    return await database.fetch_all(query, parent_id)
