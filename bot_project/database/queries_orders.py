from database.db import database
from utils.logger import logger
from decimal import Decimal
from datetime import datetime

import logging

logger = logging.getLogger(__name__)


async def get_cart_items(telegram_id: int):
    """Получает товары из корзины для данного telegram_id."""
    query = """
        SELECT
            cc.id,
            cc.quantity,
            p.id AS product_id,
            p.name,
            p.price,
            p.main_image,
            (p.price * cc.quantity) AS total
        FROM
            cart_cartitem cc
        JOIN
            products_product p ON cc.product_id = p.id
        JOIN
            core_telegramuser ctu ON cc.user_id = ctu.id
        WHERE
            ctu.telegram_id = $1;
    """
    try:
        results = await database.fetch_all(query, telegram_id)
        return [dict(row) for row in results]
    except Exception as e:
        logger.error(f"Ошибка при получении товаров из корзины: {e}")
        return []


async def create_order_db(telegram_id: int, total: float, connection):
    """Создает новый заказ и возвращает его ID."""
    query = """
        INSERT INTO orders_order (
            user_id,
            status,
            payment_status,
            address_id,
            total,
            delivery_method,
            delivery_cost,
            discount,
            promo_code,
            expected_delivery_date,
            comment,
            created_at,
            updated_at,
            is_active
        )
        VALUES (
            (SELECT id FROM core_telegramuser WHERE telegram_id = $1),  -- user_id
            'new',  -- status (по умолчанию 'new')
            'pending',  -- payment_status (по умолчанию 'pending')
            NULL,  -- address_id (пример)
            $2,  -- total
            'standard',  -- delivery_method (по умолчанию 'standard')
            0,  -- delivery_cost (по умолчанию 0)
            0,  -- discount (по умолчанию 0)
            NULL,  -- promo_code (может быть NULL)
            NULL,  -- expected_delivery_date (может быть NULL)
            NULL,  -- comment (может быть NULL)
            NOW(),  -- created_at (текущее время)
            NOW(),  -- updated_at (текущее время)
            TRUE  -- is_active (по умолчанию TRUE)
        )
        RETURNING id;
    """
    order_id = await connection.fetchval(query, telegram_id, total)
    if not order_id:
        raise ValueError("Не удалось создать заказ")
    return order_id


async def create_order_item(order_id: int, product_id: int, quantity: int, price: float, connection):
    """Добавляет элемент заказа."""
    query = """
        INSERT INTO orders_orderitem (
            order_id,
            product_id,
            quantity,
            price,
            discount,
            created_at,
            updated_at,
            is_active
        )
        VALUES (
            $1,  -- order_id
            $2,  -- product_id
            $3,  -- quantity
            $4,  -- price
            0,   -- discount (по умолчанию 0)
            NOW(),  -- created_at (текущее время)
            NOW(),  -- updated_at (текущее время)
            TRUE  -- is_active (по умолчанию TRUE)
        );
    """
    await connection.execute(query, order_id, product_id, quantity, price)


async def create_order_status_history(order_id: int, status: str, connection):
    """Добавляет запись в историю статусов заказа."""
    query = """
        INSERT INTO orders_orderstatushistory (
            order_id,
            status,
            created_at,
            updated_at,
            is_active
        )
        VALUES (
            $1,  -- order_id
            $2,  -- status
            NOW(),  -- created_at (текущее время)
            NOW(),  -- updated_at (текущее время)
            TRUE  -- is_active (по умолчанию TRUE)
        );
    """
    await connection.execute(query, order_id, status)


async def get_order_by_id(order_id: int):
    """Получает заказ по его ID."""
    try:
        logger.debug(f"Запрос в БД: получение заказа по order_id={order_id}")

        query = """
            SELECT *
            FROM orders_order
            WHERE id = $1;
        """
        order = await database.fetch_one(query, order_id)
        logger.debug(f"Результат запроса: {order}")

        if order:
            return dict(order)
        else:
            return None
    except Exception as e:
        logger.exception(f"Ошибка при получении заказа по order_id: {e}")
        return None


async def update_order_status(order_id: int, total: float):
    """Обновляет статус заказа."""
    try:
        logger.debug(
            f"Запрос в БД: обновление общей суммы заказа - order_id={order_id}, total={total}")

        query = """
            UPDATE orders_order
            SET total = $1
            WHERE id = $2;
        """
        await database.execute(query, total, order_id)
        logger.debug(
            f"Обновлена общая сумма заказа для order_id={order_id} до {total}")
        return True
    except Exception as e:
        logger.exception(f"Ошибка при обновлении общей суммы заказа: {e}")
        return False


async def update_order_payment_status(order_id: int, status: str):
    """Обновляет статус оплаты заказа."""
    try:
        logger.debug(
            f"Запрос в БД: обновление статуса оплаты заказа - order_id={order_id}, status={status}")

        query = """
            UPDATE orders_order
            SET payment_status = $1
            WHERE id = $2;
        """
        await database.execute(query, status, order_id)
        logger.debug(
            f"Обновлен статус оплаты заказа для order_id={order_id} до {status}")
        return True
    except Exception as e:
        logger.exception(f"Ошибка при обновлении статуса оплаты заказа: {e}")
        return False


async def get_cart_item(telegram_id: int, product_id: int):
    """Получает конкретный товар из корзины для данного telegram_id и product_id."""
    try:
        logger.debug(
            f"Запрос в БД: получение товара из корзины для telegram_id={telegram_id}, product_id={product_id}")

        query = """
            SELECT
                cc.id,
                cc.quantity,
                p.id AS product_id,
                p.name,
                p.price,
                p.main_image,
                (p.price * cc.quantity) AS total
            FROM
                cart_cartitem cc
            JOIN
                products_product p ON cc.product_id = p.id
            JOIN
                core_telegramuser tu ON cc.user_id = tu.id
            WHERE
                tu.telegram_id = $1 AND p.id = $2;
        """
        values = [telegram_id, product_id]

        result = await database.fetch_one(query, *values)
        logger.debug(f"Результат запроса: {result}")

        if result:
            # Преобразование Decimal в float
            result = dict(result)  # Преобразование RowProxy в словарь
            result['price'] = float(result['price']) if isinstance(
                result['price'], Decimal) else result['price']
            result['total'] = float(result['total']) if isinstance(
                result['total'], Decimal) else result['total']
            return result
        else:
            return None
    except Exception as e:
        logger.exception(f"Ошибка при получении товара из корзины: {e}")
        return None
