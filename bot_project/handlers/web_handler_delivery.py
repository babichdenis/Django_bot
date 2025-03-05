from aiohttp import web
import aiohttp_jinja2 as aioj
from database.queries_cart import (
    get_cart_by_user_id, create_cart, get_cart_item, update_cart_item_quantity,
    add_cart_item, remove_cart_item, get_cart_items, clear_cart
)
from database.queries import get_product
from utils.logger import logger


async def handle_get_cart(request):
    """Обработчик получения корзины."""
    try:
        telegram_id = int(request.query.get('telegram_id'))
        if not telegram_id:
            return web.json_response({
                "success": False,
                "message": "Не указан telegram_id"
            }, status=400)

        # Получаем корзину пользователя
        cart = await get_cart_by_user_id(telegram_id)
        if not cart:
            return web.json_response({
                "success": True,
                "total_count": 0,
                "cart_items": [],
                "total_price": 0,
            })

        # Получаем товары в корзине
        cart_items = await get_cart_items(cart['id'])

        # Преобразуем данные в JSON-совместимый формат
        cart_items_json = []
        for item in cart_items:
            cart_items_json.append({
                "id": item["id"],
                "name": item["name"],
                "price": float(item["price"]),  # Преобразуем Decimal в float
                "quantity": item["quantity"],
                "total": float(item["total"]),  # Преобразуем Decimal в float
            })

        # Считаем общую стоимость и количество товаров
        total_price = sum(item['total'] for item in cart_items)
        total_count = sum(item['quantity'] for item in cart_items)

        return web.json_response({
            "success": True,
            "total_count": total_count,
            "cart_items": cart_items_json,
            "total_price": float(total_price),  # Преобразуем Decimal в float
        })
    except Exception as e:
        logger.error(f"Ошибка в handle_get_cart: {e}")
        return web.json_response({
            "success": False,
            "message": f"Ошибка: {e}"
        }, status=500)


async def handle_add_to_cart(request):
    """Обработчик добавления товара в корзину."""
    try:
        # Получаем данные из тела запроса
        request_data = await request.json()
        telegram_id = int(request_data.get("telegram_id"))
        product_id = int(request_data.get("product_id"))
        quantity = int(request_data.get("quantity", 1))  # По умолчанию 1 товар
        print(telegram_id, product_id, quantity)
        if not telegram_id or not product_id:
            return web.json_response({
                "success": False,
                "message": "Не указан telegram_id или product_id"
            }, status=400)

          # Проверяем существование корзины
        cart = await get_cart_by_user_id(telegram_id)
        if not cart:
            cart = await create_cart(telegram_id)

        # Получаем или создаем элемент корзины
        if cart:
            cart_item = await get_cart_item(cart['id'], product_id)
            if cart_item:
                new_quantity = cart_item['quantity'] + quantity
                await update_cart_item_quantity(cart_item['id'], new_quantity)
            else:
                await add_cart_item(cart['id'], product_id, quantity)
        else:
            return web.json_response({
                "success": False,
                "message": "Ошибка при создании корзины"
            }, status=500)

        return web.json_response({
            "success": True,
            "message": "Товар добавлен в корзину"
        })
    except Exception as e:
        logger.error(f"Ошибка при добавлении товара в корзину: {e}")
        return web.json_response({
            "success": False,
            "message": f"Ошибка: {e}"
        }, status=500)


async def handle_clear_cart(request):
    """Обработчик очистки корзины."""
    try:
        request_data = await request.json()
        telegram_id = int(request_data.get("telegram_id"))
        if not telegram_id:
            return web.json_response({
                "success": False,
                "message": "Не указан telegram_id"
            }, status=400)

        # Получаем корзину пользователя
        cart = await get_cart_by_user_id(telegram_id)
        if not cart:
            return web.json_response({
                "success": False,
                "message": "Корзина не найдена"
            }, status=404)

        # Очищаем корзину
        await clear_cart(cart['id'])

        return web.json_response({
            "success": True,
            "message": "Корзина очищена"
        })
    except Exception as e:
        logger.error(f"Ошибка в handle_clear_cart: {e}")
        return web.json_response({
            "success": False,
            "message": f"Ошибка: {e}"
        }, status=500)


async def handle_update_cart_item(request):
    """Обработчик обновления количества товара в корзине."""
    try:
        request_data = await request.json()
        telegram_id = int(request_data.get("telegram_id"))
        product_id = int(request_data.get("product_id"))
        quantity = int(request_data.get("quantity"))

        if not telegram_id or not product_id or not quantity:
            return web.json_response({
                "success": False,
                "message": "Не указан telegram_id, product_id или quantity"
            }, status=400)

        # Получаем корзину пользователя
        cart = await get_cart_by_user_id(telegram_id)
        if not cart:
            return web.json_response({
                "success": False,
                "message": "Корзина не найдена"
            }, status=404)

        # Обновляем количество товара
        cart_item = await get_cart_item(cart['id'], product_id)
        if cart_item:
            await update_cart_item_quantity(cart_item['id'], quantity)
        else:
            return web.json_response({
                "success": False,
                "message": "Товар не найден в корзине"
            }, status=404)

        return web.json_response({
            "success": True,
            "message": "Количество товара обновлено"
        })
    except Exception as e:
        logger.error(f"Ошибка в handle_update_cart_item: {e}")
        return web.json_response({
            "success": False,
            "message": f"Ошибка: {e}"
        }, status=500)


async def handle_clear_cart(request):
    try:
        user_id = request.query.get('user_id')
        if not user_id:
            return web.Response(text="Не указан user_id", status=400)

        # Получаем корзину пользователя
        cart = await get_cart_by_user_id(user_id)
        if not cart:
            return web.json_response({
                'success': False,
                'message': 'Корзина не найдена'
            }, status=404)

        # Очищаем корзину
        await clear_cart(cart['id'])

        return web.json_response({
            'success': True,
            'message': 'Корзина очищена'
        })
    except Exception as e:
        logger.error(f"Ошибка в handle_clear_cart: {e}")
        return web.json_response({
            'success': False,
            'message': f"Ошибка: {e}"
        }, status=500)


async def handle_update_cart_item(request):
    """Обработчик обновления количества товара в корзине."""
    try:
        request_data = await request.json()
        telegram_id = int(request_data.get("telegram_id"))
        product_id = int(request_data.get("product_id"))
        quantity = int(request_data.get("quantity"))

        if not telegram_id or not product_id or not quantity:
            return web.json_response({
                "success": False,
                "message": "Не указан telegram_id, product_id или quantity"
            }, status=400)

        # Получаем корзину пользователя
        cart = await get_cart_by_user_id(telegram_id)
        if not cart:
            return web.json_response({
                "success": False,
                "message": "Корзина не найдена"
            }, status=404)

        # Обновляем количество товара
        cart_item = await get_cart_item(cart['id'], product_id)
        if cart_item:
            await update_cart_item_quantity(cart_item['id'], quantity)
        else:
            return web.json_response({
                "success": False,
                "message": "Товар не найден в корзине"
            }, status=404)

        return web.json_response({
            "success": True,
            "message": "Количество товара обновлено"
        })
    except Exception as e:
        logger.error(f"Ошибка в handle_update_cart_item: {e}")
        return web.json_response({
            "success": False,
            "message": f"Ошибка: {e}"
        }, status=500)
