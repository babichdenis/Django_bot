from aiohttp import web
import aiohttp_jinja2 as aioj
from database.queries_orders import (
    get_cart_items,
    create_order_db,  
    create_order_status_history,
    create_order_item,
    get_order_by_id,
    update_order_status,
    update_order_payment_status,
)
from utils.logger import logger
from database.db import database

async def handlers_create_order(request):
    """Создание нового заказа."""
    try:
        logger.info("Начало обработки запроса create_order")
        data = await request.json()
        telegram_id = data.get('telegram_id')
        if not telegram_id:
            logger.warning("Не указан telegram_id")
            return web.json_response({'error': 'User ID is required'}, status=400)

        logger.debug(f"Получен telegram_id: {telegram_id}")

        # Получаем товары из корзины
        cart_items = await get_cart_items(telegram_id)  # Передаем только telegram_id
        if not cart_items:
            logger.warning("Корзина пуста")
            return web.json_response({'error': 'Cart is empty'}, status=400)

        logger.debug(f"Товары в корзине: {cart_items}")

        # Вычисляем общую сумму заказа
        total_amount = sum(item['quantity'] * item['price'] for item in cart_items)
        logger.debug(f"Общая сумма заказа: {total_amount}")

        # Начинаем транзакцию
        async with database.pool.acquire() as connection:  # Получаем соединение из пула
            async with connection.transaction():  # Начинаем транзакцию
                # Создаем заказ
                order_id = await create_order_db(telegram_id, total_amount, connection)
                logger.debug(f"Создан заказ с order_id: {order_id}")

                # Добавляем товары в заказ
                for item in cart_items:
                    await create_order_item(order_id, item['product_id'], item['quantity'], item['price'], connection)

                # Создаем начальную запись в истории статусов
                await create_order_status_history(order_id, status='new', connection=connection)
                logger.debug("Создана запись в истории статусов")

        response_data = {'order_id': order_id}
        logger.info("Заказ успешно создан")
        return web.json_response(response_data)

    except Exception as e:
        logger.exception("Произошла ошибка при создании заказа")
        return web.json_response({'error': str(e)}, status=500)

async def handlers_order_checkout(request):
    """Оформление заказа."""
    try:
        logger.info("Начало обработки запроса order_checkout")
        order_id = int(request.match_info['order_id'])
        logger.debug(f"Получен order_id: {order_id}")

        order = await get_order_by_id(order_id)
        if not order:
            logger.warning(f"Заказ с order_id {order_id} не найден")
            return web.json_response({'error': 'Order not found'}, status=404)

        context = {'order': order}
        logger.debug(f"Контекст для шаблона: {context}")

        template = 'order_checkout.html'
        response = aioj.render_template(template, request, context)
        logger.info("Страница оформления заказа успешно отображена")
        return response

    except Exception as e:
        logger.exception("Произошла ошибка при отображении страницы оформления заказа")
        return web.json_response({'error': str(e)}, status=500)

async def handlers_order_payment(request):
    """Оплата заказа."""
    try:
        logger.info("Начало обработки запроса order_payment")
        order_id = request.match_info['order_id']
        logger.debug(f"Получен order_id: {order_id}")

        await update_order_payment_status(order_id, status='paid')
        logger.debug("Статус оплаты заказа обновлен")

        await create_order_status_history(order_id, status='processing')
        logger.debug("Создана запись в истории статусов")

        response_data = {'message': 'Order paid successfully'}
        logger.info("Оплата заказа успешно обработана")
        return web.json_response(response_data)

    except Exception as e:
        logger.exception("Произошла ошибка при обработке оплаты заказа")
        return web.json_response({'error': str(e)}, status=500)

async def handlers_order_detail(request):
    """Детали заказа."""
    try:
        logger.info("Начало обработки запроса order_detail")
        order_id = request.match_info['order_id']
        logger.debug(f"Получен order_id: {order_id}")

        order = await get_order_by_id(order_id)
        if not order:
            logger.warning(f"Заказ с order_id {order_id} не найден")
            return web.json_response({'error': 'Order not found'}, status=404)

        context = {'order': order}
        logger.debug(f"Контекст для шаблона: {context}")

        template = 'order_detail.html'
        response = aioj.render_template(template, request, context)
        logger.info("Страница деталей заказа успешно отображена")
        return response

    except Exception as e:
        logger.exception("Произошла ошибка при отображении страницы деталей заказа")
        return web.json_response({'error': str(e)}, status=500)
