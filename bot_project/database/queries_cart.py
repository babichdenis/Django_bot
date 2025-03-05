# database/queries.py
from database.db import database
from utils.logger import logger
import datetime

async def get_cart_by_user_id(user_id: int):
    """Получить корзину пользователя по его ID."""
    query = """
        SELECT c.id
        FROM cart_cart c
        JOIN core_telegramuser tu ON c.user_id = tu.id
        WHERE tu.telegram_id = $1
    """
    result = await database.fetch_one(query, user_id)
    logger.info(f"Результат запроса корзины: {result}")
    return result

async def create_cart(user_id: int):
    """Создать корзину для пользователя."""
    # Проверяем, есть ли уже корзина у пользователя
    query = "SELECT id FROM core_telegramuser WHERE telegram_id = $1"
    telegram_user_id = await database.fetchval(query, user_id)

    if not telegram_user_id:
        return None  # Пользователь не найден

    # Создаем корзину
    query = "INSERT INTO cart_cart (user_id) VALUES ($1) RETURNING id"
    cart_id = await database.fetchval(query, telegram_user_id)
    return {"id": cart_id}


async def get_cart_item(cart_id: int, product_id: int):
    """Получить элемент корзины."""
    query = "SELECT id, quantity FROM cart_cartitem WHERE cart_id = $1 AND product_id = $2"
    return await database.fetch_one(query, cart_id, product_id)

async def update_cart_item_quantity(cart_item_id: int, quantity: int):
    """Обновить количество товара в корзине."""
    now = datetime.datetime.now()
    query = """
        UPDATE cart_cartitem SET quantity = $1, updated_at = $2 WHERE id = $3
    """
    await database.execute(query, quantity, now, cart_item_id)

async def add_cart_item(cart_id: int, product_id: int, quantity: int = 1):
    """Добавить товар в корзину."""
    # Проверяем, есть ли товар уже в корзине
    item = await get_cart_item(cart_id, product_id)
    
    if item:
        # Если товар уже есть, обновляем количество
        new_quantity = item['quantity'] + quantity
        await update_cart_item_quantity(item['id'], new_quantity)
    else:
        # Если товара нет, создаем новый элемент
        now = datetime.datetime.now()
        query = """
            INSERT INTO cart_cartitem (cart_id, product_id, quantity, created_at, updated_at, is_active)
            VALUES ($1, $2, $3, $4, $5, $6)
        """
        await database.execute(query, cart_id, product_id, quantity, now, now, True)

async def remove_cart_item(cart_id: int, product_id: int):
    """Удалить товар из корзины."""
    query = "DELETE FROM cart_cartitem WHERE cart_id = $1 AND product_id = $2"
    try:
        logger.info(f"Попытка удаления товара: cart_id={cart_id}, product_id={product_id}")
        await database.execute(query, cart_id, product_id)


async def get_cart_items(cart_id: int):
    """Получить все товары в корзине."""
    query = """SELECT ci.id, p.name, p.price, ci.quantity, (p.price * ci.quantity) AS total
               FROM cart_cartitem ci
               JOIN products_product p ON ci.product_id = p.id
               WHERE ci.cart_id = $1"""
    return await database.fetch_all(query, cart_id)

async def clear_cart(cart_id: int):
    """Очистить корзину."""
    query = "DELETE FROM cart_cartitem WHERE cart_id = $1"
    await database.execute(query, cart_id)
