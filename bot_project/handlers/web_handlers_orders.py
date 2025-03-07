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
from utils.utils import generate_csrf_token
from aiohttp_session import get_session
from yookassa import Payment
import uuid


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
        cart_items = await get_cart_items(telegram_id)
        if not cart_items:
            logger.warning("Корзина пуста")
            return web.json_response({'error': 'Cart is empty'}, status=400)

        logger.debug(f"Товары в корзине: {cart_items}")

        # Вычисляем общую сумму заказа
        total_amount = sum(item['quantity'] * item['price'] for item in cart_items)
        logger.debug(f"Общая сумма заказа: {total_amount}")

        async with database.pool.acquire() as connection:
            async with connection.transaction():  

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

        # Получение заказа
        order = await get_order_by_id(order_id)
        if not order:
            logger.warning(f"Заказ с order_id {order_id} не найден")
            return web.json_response({'error': 'Order not found'}, status=404)

        # Генерация CSRF-токена
        csrf_token = generate_csrf_token()

        # Сохранение токена в сессии (если используется aiohttp-session)
        session = await get_session(request)
        session['csrf_token'] = csrf_token

        # Подготовка контекста для шаблона
        context = {
            'order': order,
            'csrf_token': csrf_token,  # Передача токена в шаблон
        }
        logger.debug(f"Контекст для шаблона: {context}")

        # Отображение шаблона
        template = 'order_checkout.html'
        response = aioj.render_template(template, request, context)
        logger.info("Страница оформления заказа успешно отображена")
        return response

    except Exception as e:
        logger.exception("Произошла ошибка при отображении страницы оформления заказа")
        return web.json_response({'error': str(e)}, status=500)


async def create_payment(order_id, amount):
    """
    Создает платеж в ЮKassa.
    """
    payment = Payment.create({
        "amount": {
            "value": str(amount), 
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://your-site.com/payment-result"  
        "capture": True,
        "description": f"Оплата заказа №{order_id}",
        "metadata": {
            "order_id": order_id
        }
    }, str(uuid.uuid4())})  # Уникальный идентификатор платежа

    return payment


async def handlers_order_payment(request):
    """Оплата заказа."""
    try:
        # Проверка CSRF-токена
        data = await request.post()
        csrf_token = data.get('csrf_token')
        session = await get_session(request)
        if 'csrf_token' not in session or session['csrf_token'] != csrf_token:
            logger.warning("Неверный CSRF-токен")
            return web.json_response({'error': 'Invalid CSRF token'}, status=400)

        # Получение заказа
        order_id = int(request.match_info['order_id'])
        order = await get_order_by_id(order_id)
        if not order:
            logger.warning(f"Заказ с order_id {order_id} не найден")
            return web.json_response({'error': 'Order not found'}, status=404)

        # Создание платежа
        payment = await create_payment(order.id, order.total)
        confirmation_url = payment.confirmation.confirmation_url

        # Перенаправление пользователя на страницу оплаты
        return web.HTTPFound(confirmation_url)

    except Exception as e:
        logger.exception("Произошла ошибка при обработке оплаты")
        return web.json_response({'error': str(e)}, status=500)


async def handle_yookassa_webhook(request):
    """Обработка уведомлений от ЮKassa."""
    try:
        data = await request.json()
        payment_id = data['object']['id']
        status = data['object']['status']

        # Получение order_id из метаданных
        order_id = data['object']['metadata']['order_id']

        # Обновление статуса заказа в базе данных
        await update_order_status(order_id, status)

        return web.Response(status=200)
    except Exception as e:
        logger.exception("Ошибка при обработке уведомления от ЮKassa")
        return web.Response(status=500)


async def update_order_status(order_id, status):
    """
    Обновляет статус заказа в базе данных.
    """
    pass
    logger.info(f"Обновление статуса заказа {order_id} на {status}")


async def payment_result(request):
    """Отображение результата платежа."""
    try:
        payment_id = request.query.get('payment_id')
        order_id = request.query.get('order_id')

        payment = Payment.find_one(payment_id)
        payment_success = payment.status == 'succeeded'

        context = {
            'payment_success': payment_success,
            'order': await get_order_by_id(order_id),
        }
        return web.Response(text=render_template('payment_result.html', context))
    except Exception as e:
        logger.exception("Ошибка при отображении результата платежа")
        return web.json_response({'error': str(e)}, status=500)
