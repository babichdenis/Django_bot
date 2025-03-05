from aiohttp import web
from .logger import logger
from decimal import Decimal

async def handle_error(error_message, status=500):
    """Логирует ошибку и возвращает HTTP-ответ."""
    logger.error(error_message)
    return web.Response(text="Internal Server Error", status=status)


def decimal_to_float(data):
    """Преобразует Decimal в float для JSON-сериализации."""
    if isinstance(data, dict):
        return {key: decimal_to_float(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [decimal_to_float(item) for item in data]
    elif isinstance(data, Decimal):
        return float(data) 
    return data
