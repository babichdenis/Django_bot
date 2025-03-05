from aiohttp import web
import aiohttp_jinja2 as aioj
from database.queries_cart import (
    get_cart_by_user_id, create_cart, get_cart_item, update_cart_item_quantity,
    add_cart_item, remove_cart_item, get_cart_items, clear_cart
)
from database.queries import get_product
from utils.logger import logger
from utils.utils import decimal_to_float


async def handle_get_cart(request):
    """Обработчик получения корзины."""
    try:
        logger.info("Начало обработки запроса handle_get_cart")
        telegram_id = int(request.query.get('telegram_id'))
        logger.info(f"Получен telegram_id: {telegram_id}")

        if not telegram_id:
            logger.error("Не указан telegram_id")
            return web.json_response({
                "success": False,
                "message": "Не указан telegram_id"
            }, status=400)

        # Получаем корзину пользователя
        logger.info(f"Поиск корзины для пользователя с telegram_id: {telegram_id}")
        cart = await get_cart_by_user_id(telegram_id)
        logger.info(f"Результат поиска корзины: {cart}")

        if not cart:
            logger.info("Корзина не найдена, возвращаем пустую корзину")
            return web.json_response({
                "success": True,
                "total_count": 0,
                "cart_items": [],
                "total_price": 0,
            })

        # Получаем товары в корзине
        logger.info(f"Получение товаров в корзине для cart_id: {cart['id']}")
        cart_items = await get_cart_items(cart['id'])
        logger.info(f"Товары в корзине: {cart_items}")

        # Преобразуем данные в JSON-совместимый формат
        cart_items_json = []
        for item in cart_items:
            cart_items_json.append({
                "id": int(item["id"]),
                "name": item["name"],
                "price": float(item["price"]),  # Преобразуем Decimal в float
                "quantity": int(item["quantity"]),
                "total": float(item["total"]),  # Преобразуем Decimal в float
            })

        # Считаем общую стоимость и количество товаров
        total_price = sum(float(item['total']) for item in cart_items)
        total_count = sum(int(item['quantity']) for item in cart_items)
        logger.info(f"Общая стоимость: {total_price}, Общее количество: {total_count}")

        return web.json_response({
            "success": True,
            "total_count": int(total_count),
            "cart_items": cart_items_json,
            "total_price": float(total_price),
        })
    except Exception as e:
        logger.error(f"Ошибка в handle_get_cart: {e}", exc_info=True)
        return web.json_response({
            "success": False,
            "message": f"Ошибка: {e}"
        }, status=500)


async def handle_add_to_cart(request):
    """Обработчик добавления товара в корзину."""
    try:
        logger.info("Начало обработки запроса handle_add_to_cart")
        # Получаем данные из тела запроса
        request_data = await request.json()
        telegram_id = int(request_data.get("telegram_id"))
        product_id = int(request_data.get("product_id"))
        quantity = int(request_data.get("quantity", 1))  # По умолчанию 1 товар
        logger.info(f"Полученные данные: telegram_id={telegram_id}, product_id={product_id}, quantity={quantity}")

        if not telegram_id or not product_id:
            logger.error("Не указан telegram_id или product_id")
            return web.json_response({
                "success": False,
                "message": "Не указан telegram_id или product_id"
            }, status=400)

        # Проверяем существование корзины
        logger.info(f"Поиск корзины для пользователя с telegram_id: {telegram_id}")
        cart = await get_cart_by_user_id(telegram_id)
        logger.info(f"Результат поиска корзины: {cart}")

        if not cart:
            logger.info("Корзина не найдена, создаем новую корзину")
            cart = await create_cart(telegram_id)
            logger.info(f"Созданная корзина: {cart}")

        # Получаем или создаем элемент корзины
        if cart:
            logger.info(f"Поиск товара в корзине: cart_id={cart['id']}, product_id={product_id}")
            cart_item = await get_cart_item(cart['id'], product_id)
            logger.info(f"Результат поиска товара в корзине: {cart_item}")

            if cart_item:
                new_quantity = int(cart_item['quantity']) + quantity
                logger.info(f"Обновление количества товара: новое количество={new_quantity}")
                await update_cart_item_quantity(cart_item['id'], new_quantity)
            else:
                logger.info("Добавление нового товара в корзину")
                await add_cart_item(cart['id'], product_id, quantity)
        else:
            logger.error("Ошибка при создании корзины")
            return web.json_response({
                "success": False,
                "message": "Ошибка при создании корзины"
            }, status=500)

        logger.info("Товар успешно добавлен в корзину")
        return web.json_response({
            "success": True,
            "message": "Товар добавлен в корзину"
        })
    except Exception as e:
        logger.error(f"Ошибка при добавлении товара в корзину: {e}", exc_info=True)
        return web.json_response({
            "success": False,
            "message": f"Ошибка: {e}"
        }, status=500)


async def handle_clear_cart(request):
    """Обработчик очистки корзины."""
    try:
        logger.info("Начало обработки запроса handle_clear_cart")
        request_data = await request.json()
        telegram_id = int(request_data.get("telegram_id"))
        logger.info(f"Полученный telegram_id: {telegram_id}")

        if not telegram_id:
            logger.error("Не указан telegram_id")
            return web.json_response({
                "success": False,
                "message": "Не указан telegram_id"
            }, status=400)

        # Получаем корзину пользователя
        logger.info(f"Поиск корзины для пользователя с telegram_id: {telegram_id}")
        cart = await get_cart_by_user_id(telegram_id)
        logger.info(f"Результат поиска корзины: {cart}")

        if not cart:
            logger.error("Корзина не найдена")
            return web.json_response({
                "success": False,
                "message": "Корзина не найдена"
            }, status=404)

        # Очищаем корзину
        logger.info(f"Очистка корзины с cart_id: {cart['id']}")
        await clear_cart(cart['id'])

        logger.info("Корзина успешно очищена")
        return web.json_response({
            "success": True,
            "message": "Корзина очищена"
        })
    except Exception as e:
        logger.error(f"Ошибка в handle_clear_cart: {e}", exc_info=True)
        return web.json_response({
            "success": False,
            "message": f"Ошибка: {e}"
        }, status=500)


async def handle_update_cart_item(request):
    """Обработчик обновления количества товара в корзине."""
    try:
        logger.info("Начало обработки запроса handle_update_cart_item")
        request_data = await request.json()
        telegram_id = int(request_data.get("telegram_id"))
        product_id = int(request_data.get("product_id"))
        quantity = int(request_data.get("quantity"))
        logger.info(f"Полученные данные: telegram_id={telegram_id}, product_id={product_id}, quantity={quantity}")

        if not telegram_id or not product_id or not quantity:
            logger.error("Не указан telegram_id, product_id или quantity")
            return web.json_response({
                "success": False,
                "message": "Не указан telegram_id, product_id или quantity"
            }, status=400)

        # Получаем корзину пользователя
        logger.info(f"Поиск корзины для пользователя с telegram_id: {telegram_id}")
        cart = await get_cart_by_user_id(telegram_id)
        logger.info(f"Результат поиска корзины: {cart}")

        if not cart:
            logger.error("Корзина не найдена")
            return web.json_response({
                "success": False,
                "message": "Корзина не найдена"
            }, status=404)

        # Обновляем количество товара
        logger.info(f"Поиск товара в корзине: cart_id={cart['id']}, product_id={product_id}")
        cart_item = await get_cart_item(cart['id'], product_id)
        logger.info(f"Результат поиска товара в корзине: {cart_item}")

        if cart_item:
            logger.info(f"Обновление количества товара: новое количество={quantity}")
            await update_cart_item_quantity(cart_item['id'], quantity)
        else:
            logger.error("Товар не найден в корзине")
            return web.json_response({
                "success": False,
                "message": "Товар не найден в корзине"
            }, status=404)

        # Получаем обновленные данные корзины
        logger.info("Получение обновленных данных корзины")
        cart_items = await get_cart_items(cart['id'])
        total_price = sum(float(item['total']) for item in cart_items)
        logger.info(f"Обновленные данные корзины: cart_items={cart_items}, total_price={total_price}")

        return web.json_response({
            "success": True,
            "message": "Количество товара обновлено",
            "cart_items": cart_items,
            "total_price": float(total_price),
        })
    except Exception as e:
        logger.error(f"Ошибка в handle_update_cart_item: {e}", exc_info=True)
        return web.json_response({
            "success": False,
            "message": f"Ошибка: {e}"
        }, status=500)


async def handle_remove_from_cart(request):
    """Обработчик удаления товара из корзины."""
    try:
        logger.info("Начало обработки запроса handle_remove_from_cart")
        # Получаем данные из запроса
        request_data = await request.json()
        telegram_id = int(request_data.get("telegram_id"))
        product_id = int(request_data.get("product_id"))
        logger.info(f"Полученные данные: telegram_id={telegram_id}, product_id={product_id}")

        # Валидация данных
        if not telegram_id or not product_id:
            logger.error("Не указан telegram_id или product_id")
            return web.json_response({
                "success": False,
                "message": "Не указан telegram_id или product_id"
            }, status=400)

        # Получаем корзину пользователя
        logger.info(f"Поиск корзины для пользователя с telegram_id: {telegram_id}")
        cart = await get_cart_by_user_id(telegram_id)
        logger.info(f"Результат поиска корзины: {cart}")

        if not cart:
            logger.error("Корзина не найдена")
            return web.json_response({
                "success": False,
                "message": "Корзина не найдена"
            }, status=404)

        # Удаляем товар из корзины
        logger.info(f"Удаление товара из корзины: cart_id={cart['id']}, product_id={product_id}")
        await remove_cart_item(cart['id'], product_id)

        # Возвращаем обновленные данные корзины
        logger.info("Получение обновленных данных корзины")
        cart_items = await get_cart_items(cart['id'])
        total_price = sum(float(item['total']) for item in cart_items)
        logger.info(f"Обновленные данные корзины: cart_items={cart_items}, total_price={total_price}")

        # Преобразуем Decimal в float
        cart_items_list = [decimal_to_float(dict(item)) for item in cart_items]
        total_price = float(total_price)
        logger.info(f"Преобразованные данные: cart_items_list={cart_items_list}, total_price={total_price}")

        return web.json_response({
            "success": True,
            "cart_items": cart_items_list,
            "total_price": total_price
        })
    except Exception as e:
        logger.error(f"Ошибка в handle_remove_from_cart: {e}", exc_info=True)
        return web.json_response({
            "success": False,
            "message": f"Internal Server Error: {str(e)}"
        }, status=500)
