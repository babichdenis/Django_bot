from aiohttp import web
import aiohttp_jinja2 as aioj
from database.queries_cart import (
    get_cart_item,
    get_cart_items,
    add_cart_item,
    update_cart_item_quantity,
    remove_cart_item,
    clear_cart
)
from database.queries_orders import (
    create_order_db,
    create_order_item,
    create_order_status_history,
    get_order_by_id,
    update_order_status,
    update_order_payment_status
)
from utils.logger import logger
from utils.utils import decimal_to_float

async def handle_get_cart(request):
    """Обработчик получения корзины."""
    try:
        logger.info("Начало обработки запроса handle_get_cart")
        telegram_id = request.query.get('telegram_id')
        if telegram_id is None:
            logger.error("Не указан telegram_id")
            return web.json_response({
                "success": False,
                "message": "Не указан telegram_id"
            }, status=400)

        telegram_id = int(telegram_id)
        logger.info(f"Получен telegram_id: {telegram_id}")

        # Получаем товары в корзине
        cart_items = await get_cart_items(telegram_id)
        cart_items_json = []
        total_price = 0
        total_count = 0
        print(cart_items)
        for item in cart_items:
            cart_items_json.append({
                "id": item["id"],
                "name": item["name"],
                "price": float(item["price"]),
                "quantity": item["quantity"],
                "total": float(item["total"]),
            })
            total_price += float(item["total"])
            total_count += item["quantity"]

        return web.json_response({
            "success": True,
            "total_count": total_count,
            "cart_items": cart_items_json,
            "total_price": total_price,
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
        request_data = await request.json()
        telegram_id = request_data.get("telegram_id")
        product_id = request_data.get("product_id")
        quantity = request_data.get("quantity", 1)

        if telegram_id is None or product_id is None:
            logger.error("Не указан telegram_id или product_id")
            return web.json_response({
                "success": False,
                "message": "Не указан telegram_id или product_id"
            }, status=400)

        telegram_id = int(telegram_id)
        product_id = int(product_id)
        quantity = int(quantity)

        await add_cart_item(telegram_id, product_id, quantity)

        return web.json_response({
            "success": True,
            "message": "Товар добавлен в корзину"
        })
    except Exception as e:
        logger.error(f"Ошибка в handle_add_to_cart: {e}", exc_info=True)
        return web.json_response({
            "success": False,
            "message": f"Ошибка: {e}"
        }, status=500)


async def handle_remove_from_cart(request):
    """Обработчик удаления товара из корзины."""
    try:
        logger.info("Начало обработки запроса handle_remove_from_cart")
        request_data = await request.json()
        telegram_id = request_data.get("telegram_id")
        product_id = request_data.get("product_id")

        if telegram_id is None or product_id is None:
            logger.error("Не указан telegram_id или product_id")
            return web.json_response({
                "success": False,
                "message": "Не указан telegram_id или product_id"
            }, status=400)

        telegram_id = int(telegram_id)
        product_id = int(product_id)

        await remove_cart_item(telegram_id, product_id)

        return web.json_response({
            "success": True,
            "message": "Товар удален из корзины"
        })
    except Exception as e:
        logger.error(f"Ошибка в handle_remove_from_cart: {e}", exc_info=True)
        return web.json_response({
            "success": False,
            "message": f"Ошибка: {e}"
        }, status=500)


async def handle_update_cart_item(request):
    """Обработчик обновления количества товара в корзине."""
    try:
        logger.info("Начало обработки запроса handle_update_cart_item")
        request_data = await request.json()
        telegram_id = request_data.get("telegram_id")
        product_id = request_data.get("product_id")
        change = request_data.get("change")  # Изменение количества (например, +1 или -1)

        if telegram_id is None or product_id is None or change is None:
            logger.error("Не указан telegram_id, product_id или change")
            return web.json_response({
                "success": False,
                "message": "Не указан telegram_id, product_id или change"
            }, status=400)

        telegram_id = int(telegram_id)
        product_id = int(product_id)
        change = int(change)

        # Получаем текущий элемент корзины
        cart_item = await get_cart_item(telegram_id, product_id)
        if cart_item is None:
            logger.error("Товар не найден в корзине")
            return web.json_response({
                "success": False,
                "message": "Товар не найден в корзине"
            }, status=404)

        # Вычисляем новое количество
        new_quantity = cart_item["quantity"] + change

        # Проверяем, чтобы количество не было меньше 1
        if new_quantity < 1:
            new_quantity = 1

        # Обновляем количество товара в корзине
        await update_cart_item_quantity(cart_item["id"], new_quantity)

        # Получаем обновленные данные корзины
        cart_items = await get_cart_items(telegram_id)
        cart_items_json = []
        total_price = 0
        total_count = 0

        for item in cart_items:
            cart_items_json.append({
                "id": item["id"],
                "name": item["name"],
                "price": float(item["price"]),
                "quantity": item["quantity"],
                "total": float(item["total"]),
            })
            total_price += float(item["total"])
            total_count += item["quantity"]

        return web.json_response({
            "success": True,
            "message": "Количество товара обновлено",
            "cart_items": cart_items_json,
            "total_price": total_price,
        })
    except Exception as e:
        logger.error(f"Ошибка в handle_update_cart_item: {e}", exc_info=True)
        return web.json_response({
            "success": False,
            "message": f"Ошибка: {e}"
        }, status=500)


async def handle_clear_cart(request):
    """Обработчик очистки корзины."""
    try:
        logger.info("Начало обработки запроса handle_clear_cart")
        request_data = await request.json()
        telegram_id = request_data.get("telegram_id")

        if telegram_id is None:
            logger.error("Не указан telegram_id")
            return web.json_response({
                "success": False,
                "message": "Не указан telegram_id"
            }, status=400)

        telegram_id = int(telegram_id)

        await clear_cart(telegram_id)

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



async def handle_cart_page(request):
    """Обработчик для отображения страницы корзины."""
    try:
        telegram_id = request.query.get('telegram_id')

        if telegram_id is None:
            return aioj.render_template("cart.html", request, {
                "cart_items": [],
                "total_price": 0,
                "telegram_id": None,
                "category": None,
                "error_message": "Не указан telegram_id"
            })

        telegram_id = int(telegram_id)

        cart_items = await get_cart_items(telegram_id)
        total_price = sum(item['total'] for item in cart_items)

        # Преобразуем данные для шаблона
        cart_items_json = [
            {
                "id": item['id'],
                "product_id": item['product_id'],
                "name": item['name'],
                "price": item['price'],
                "image": item['main_image'],  # Передаем URL изображения
                "quantity": item['quantity'],
                "total": item['total']
            }
            for item in cart_items
        ]

        return aioj.render_template("cart.html", request, {
            "cart_items": cart_items_json,
            "total_price": total_price,
            "telegram_id": telegram_id,
            "category": None
        })
    except Exception as e:
        # Обработка ошибок
        return aioj.render_template("cart.html", request, {
            "cart_items": [],
            "total_price": 0,
            "telegram_id": None,
            "category": None,
            "error_message": str(e)  # Передаем сообщение об ошибке в шаблон
        })


async def create_order(request):
    """Создание нового заказа."""
    try:
        logger.info("Начало обработки запроса create_order")
        data = await request.json()
        telegram_id = data.get('telegram_id')  # Получаем telegram_id
        if not telegram_id:
            logger.warning("Не указан telegram_id")
            return web.json_response({'error': 'telegram_id is required'}, status=400)

        # Получаем user_id из таблицы core_telegramuser по telegram_id
        query = "SELECT id FROM core_telegramuser WHERE telegram_id = $1"
        user_id_row = await request.app['db'].fetch_one(query, telegram_id)
        if not user_id_row:
            logger.warning(f"Пользователь с telegram_id {telegram_id} не найден")
            return web.json_response({'error': 'User not found'}, status=404)

        user_id = user_id_row[0]  # Получаем id пользователя

        logger.debug(f"Получен user_id: {user_id}")

        # Получаем товары из корзины
        cart_items = await get_cart_items(user_id)  # Передаем user_id
        if not cart_items:
            logger.warning("Корзина пуста")
            return web.json_response({'error': 'Cart is empty'}, status=400)

        logger.debug(f"Товары в корзине: {cart_items}")

        # Создаем заказ
        total_amount = sum(item['quantity'] * item['price'] for item in cart_items) # Считаем сумму заказа
        order_id = await create_order_db(user_id, total_amount)  # Передаем user_id и сумму заказа
        if not order_id:
            logger.error("Не удалось создать заказ")
            return web.json_response({'error': 'Failed to create order'}, status=500)
        logger.debug(f"Создан заказ с order_id: {order_id}")

        # Добавляем товары в заказ
        for item in cart_items:
            success = await create_order_item(order_id, item['product_id'], item['quantity'], item['price'])
            if not success:
                logger.error(f"Не удалось создать элемент заказа для product_id={item['product_id']}")
                # Обработка ошибки создания элемента заказа (например, откат транзакции)
                return web.json_response({'error': 'Failed to create order item'}, status=500)
        logger.debug("Элементы заказа успешно созданы")

        # Создаем начальную запись в истории статусов
        success = await create_order_status_history(order_id, status='new')
        if not success:
            logger.error("Не удалось создать запись в истории статусов")
            return web.json_response({'error': 'Failed to create order status history'}, status=500)
        logger.debug("Создана запись в истории статусов")

        response_data = {'order_id': order_id}
        logger.info("Заказ успешно создан")
        return web.json_response(response_data)

    except Exception as e:
        logger.exception("Произошла ошибка при создании заказа")
        return web.json_response({'error': str(e)}, status=500)
