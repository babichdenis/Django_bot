from aiohttp import web
from handlers.web_handlers import (
    handle_index,
    handle_category,
    handle_product
)
from handlers.web_handler_cart import (
    handle_get_cart,
    handle_add_to_cart,
    handle_remove_from_cart,
    handle_update_cart_item,
    handle_clear_cart,
    handle_cart_page
)

def setup_web_routes(app: web.Application, media_dir: str):
    """Настройка веб-маршрутов"""
    app.add_routes([
        web.get("/", handle_index),
        web.get("/category/{category_id}", handle_category),
        web.get("/product/{product_id}", handle_product),
        web.get("/cart", handle_cart_page),
        web.get("/get-cart", handle_get_cart),
        web.post("/add-to-cart", handle_add_to_cart),
        web.post("/remove-from-cart", handle_remove_from_cart),
        web.post("/update-cart-item", handle_update_cart_item),
        web.post("/clear-cart", handle_clear_cart),
        web.static("/media", media_dir),
    ])
