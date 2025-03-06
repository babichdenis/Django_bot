# database/queries_cart.py
from utils.logger import logger
from database.db import database
from datetime import datetime

async def get_cart_item(telegram_id: int, product_id: int):
    """Получить элемент корзины по telegram_id и product_id."""
    query = """
        SELECT cc.id, p.name, p.price, cc.quantity, (p.price * cc.quantity) AS total
        FROM cart_cartitem cc
        JOIN products_product p ON cc.product_id = p.id
        JOIN core_telegramuser u ON cc.user_id = u.id
        WHERE u.telegram_id = $1 AND cc.product_id = $2
    """
    logger.debug(f"Executing get_cart_item query with telegram_id={telegram_id}, product_id={product_id}")
    result = await database.fetch_one(query, telegram_id, product_id)
    if result:
        logger.debug(f"get_cart_item result: {result}")
    else:
        logger.debug("get_cart_item: Item not found")
    return result

async def get_cart_items(telegram_id: int):
    """Получить все элементы корзины для данного telegram_id."""
    query = """
        SELECT cc.id, cc.product_id, p.name, p.price, p.main_image, cc.quantity, (p.price * cc.quantity) AS total
        FROM cart_cartitem cc
        JOIN products_product p ON cc.product_id = p.id
        JOIN core_telegramuser u ON cc.user_id = u.id
        WHERE u.telegram_id = $1
    """
    logger.debug(f"Executing get_cart_items query with telegram_id={telegram_id}")
    return await database.fetch_all(query, telegram_id)


async def add_cart_item(telegram_id: int, product_id: int, quantity: int = 1):
    """Добавить товар в корзину."""
    # Получаем user_id на основе telegram_id
    query_user = "SELECT id FROM core_telegramuser WHERE telegram_id = $1"
    user_id = await database.fetchval(query_user, telegram_id)

    # Проверяем, есть ли уже элемент корзины для данного товара
    existing_cart_item = await get_cart_item(telegram_id, product_id)

    if existing_cart_item:
        # Если элемент уже существует, обновляем количество
        new_quantity = existing_cart_item['quantity'] + quantity
        await update_cart_item_quantity(existing_cart_item['id'], new_quantity)
    else:
        # Если элемента нет, создаем новый
        now = datetime.now()
        query = """
            INSERT INTO cart_cartitem (user_id, product_id, quantity, created_at, updated_at, is_active)
            VALUES ($1, $2, $3, $4, $5, TRUE)
        """
        logger.debug(f"Executing add_cart_item query with user_id={user_id}, product_id={product_id}, quantity={quantity}")
        await database.execute(query, user_id, product_id, quantity, now, now)

async def update_cart_item_quantity(cart_item_id: int, quantity: int):
    """Обновить количество товара в корзине."""
    now = datetime.now()
    query = """
        UPDATE cart_cartitem
        SET quantity = $1, updated_at = $2
        WHERE id = $3
    """
    logger.debug(f"Executing update_cart_item_quantity query with cart_item_id={cart_item_id}, quantity={quantity}")
    await database.execute(query, quantity, now, cart_item_id)

async def remove_cart_item(telegram_id: int, product_id: int):
    """Удалить товар из корзины."""
    # Получаем user_id на основе telegram_id
    query_user = "SELECT id FROM core_telegramuser WHERE telegram_id = $1"
    user_id = await database.fetchval(query_user, telegram_id)
    query = """
        DELETE FROM cart_cartitem
        WHERE user_id = $1 AND product_id = $2
    """
    logger.debug(f"Executing remove_cart_item query with user_id={user_id}, product_id={product_id}")
    await database.execute(query, user_id, product_id)

async def clear_cart(telegram_id: int):
    """Очистить корзину для данного telegram_id."""
    # Получаем user_id на основе telegram_id
    query_user = "SELECT id FROM core_telegramuser WHERE telegram_id = $1"
    user_id = await database.fetchval(query_user, telegram_id)
    query = """
        DELETE FROM cart_cartitem
        WHERE user_id = $1
    """
    logger.debug(f"Executing clear_cart query with user_id={user_id}")
    await database.execute(query, user_id)
