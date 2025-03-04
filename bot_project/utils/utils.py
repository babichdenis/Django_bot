from aiohttp import web
from logger import logger

async def handle_error(error_message, status=500):
    """Логирует ошибку и возвращает HTTP-ответ."""
    logger.error(error_message)
    return web.Response(text="Internal Server Error", status=status)
