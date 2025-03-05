# database/db.py
import asyncpg
from decouple import config
from utils.logger import logger

class Database:
    def __init__(self):
        """Конструктор класса, инициализирующий конфигурацию."""
        self.pool = None

    async def connect(self):
        """Инициализация пула подключений к базе данных."""
        try:
            self.pool = await asyncpg.create_pool(
                host=config("DB_HOST"),
                port=config("DB_PORT", cast=int),
                user=config("DB_USER"),
                password=config("DB_PASSWORD"),
                database=config("DB_NAME"),
            )
            logger.info("Database connection pool created")
        except Exception as e:
            logger.critical(f"Database connection error: {e}")
            raise


    async def execute(self, query: str, *args):
        """Выполнить SQL-запрос."""
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)
            
    async def fetch_all(self, query, *args):
        """Выполнить запрос и вернуть все результаты."""
        async with self.pool.acquire() as conn:
            try:
                return await conn.fetch(query, *args)
            except Exception as e:
                logger.error(f"Query error: {query} | {e}")
                return []

    async def fetch_one(self, query, *args):
        """Выполнить запрос и вернуть одну запись."""
        async with self.pool.acquire() as conn:
            try:
                return await conn.fetchrow(query, *args)
            except Exception as e:
                logger.error(f"Query error: {query} | {e}")
                return None

    async def fetchval(self, query, *args):
        """Выполнить запрос и вернуть одно значение."""
        async with self.pool.acquire() as conn:
            try:
                return await conn.fetchval(query, *args)
            except Exception as e:
                logger.error(f"Query error: {query} | {e}")
                return None

# Создание экземпляра базы данных
database = Database()
