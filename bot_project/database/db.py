# database/db.py
import asyncpg
from decouple import config
from utils.logger import logger

class Database:
    def __init__(self):
        """Конструктор класса, инициализирующий конфигурацию."""
        self.pool = None
        logger.debug("Database instance created")

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
        logger.debug(f"Executing query: {query} with args: {args}")
        async with self.pool.acquire() as conn:
            try:
                result = await conn.execute(query, *args)
                logger.debug(f"Query executed successfully: {query}")
                return result
            except Exception as e:
                logger.error(f"Query execution error: {query} | {e}")
                raise

    async def fetch_all(self, query, *args):
        """Выполнить запрос и вернуть все результаты."""
        logger.debug(f"Fetching all with query: {query} and args: {args}")
        async with self.pool.acquire() as conn:
            try:
                result = await conn.fetch(query, *args)
                logger.debug(f"Query fetched successfully: {query} | Result count: {len(result)}")
                return result
            except Exception as e:
                logger.error(f"Query error: {query} | {e}")
                return []

    async def fetch_one(self, query, *args):
        """Выполнить запрос и вернуть одну запись."""
        logger.debug(f"Fetching one with query: {query} and args: {args}")
        async with self.pool.acquire() as conn:
            try:
                result = await conn.fetchrow(query, *args)
                if result:
                    logger.debug(f"Query fetched successfully: {query} | Result: {result}")
                else:
                    logger.debug(f"Query fetched successfully: {query} | Result: None")
                return result
            except Exception as e:
                logger.error(f"Query error: {query} | {e}")
                return None

    async def fetchval(self, query, *args):
        """Выполнить запрос и вернуть одно значение."""
        logger.debug(f"Fetching val with query: {query} and args: {args}")
        async with self.pool.acquire() as conn:
            try:
                result = await conn.fetchval(query, *args)
                if result:
                    logger.debug(f"Query fetched successfully: {query} | Result: {result}")
                else:
                    logger.debug(f"Query fetched successfully: {query} | Result: None")
                return result
            except Exception as e:
                logger.error(f"Query error: {query} | {e}")
                return None

# Создание экземпляра базы данных
database = Database()
