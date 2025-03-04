import asyncpg
from logger import logger

# Настройки базы данных
DB_CONFIG = {
    "host": "localhost",
    "user": "user",
    "password": "password",
    "database": "postgres",
    "port": "5433",
}

pool = None

async def create_pool():
    global pool
    try:
        pool = await asyncpg.create_pool(**DB_CONFIG)
        logger.info("Database connection pool created")
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise

async def get_categories():
    async with pool.acquire() as conn:
        try:
            return await conn.fetch("SELECT id, name, image FROM products_category")
        except Exception as e:
            logger.error(f"Error fetching categories: {e}")
            return []

async def get_products_by_category(category_id):
    async with pool.acquire() as conn:
        try:
            return await conn.fetch(
                """SELECT p.id, p.name, p.price, p.description, p.main_image
                   FROM products_product p
                   JOIN products_product_categories pc ON p.id = pc.product_id
                   WHERE pc.category_id = $1""", 
                category_id
            )
        except Exception as e:
            logger.error(f"Error fetching products: {e}")
            return []

async def get_featured_products(limit=5):
    async with pool.acquire() as conn:
        try:
            return await conn.fetch(
                """SELECT id, name, price, main_image as image
                   FROM products_product
                   ORDER BY created_at DESC
                   LIMIT $1""",
                limit
            )
        except Exception as e:
            logger.error(f"Error fetching featured products: {e}")
            return []
