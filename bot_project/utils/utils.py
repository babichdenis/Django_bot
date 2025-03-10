import secrets
from aiohttp import web
from .logger import logger
from functools import wraps


def handle_errors(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        try:
            return await func(request, *args, **kwargs)
        except ValueError as e:
            logger.error(f"ValueError in {func.__name__}: {e}")
            return web.Response(text="Invalid request data", status=400)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
            return web.Response(text="Internal Server Error", status=500)
    return wrapper


def generate_csrf_token():
    """
    Генерирует случайный CSRF-токен.
    """
    return secrets.token_hex(16)
