# handlers/web_handlers.py
from aiohttp import web
import aiohttp_jinja2 as aioj
from database.queries import (
    get_categories,
    get_category,
    get_products_by_category,
    get_featured_products,
    get_product,
    product_exists,
    get_total_products_by_category  # Импортируем новую функцию
)
from utils.logger import logger
from utils.utils import handle_error
from database.db import database


async def handle_index(request):
    """Главная страница с популярными товарами."""
    try:
        context = {
            "featured_products": await get_featured_products(),
            "categories": await get_categories(),
        }
        return aioj.render_template("index.html", request, context)
    except Exception as e:
        logger.error(f"Index handler error: {e}")
        return web.Response(text="Service Unavailable", status=503)

async def handle_product(request):
    """Страница товара."""
    try:
        product_id = int(request.match_info["product_id"])
        if not await product_exists(product_id):
            return web.Response(text="Product not found", status=404)

        product = await get_product(product_id)
        if product is None:
            return web.Response(text="Product not available", status=410)

        # Получить категорию товара
        category_id = product['category_id']
        category = await get_category(category_id)

        # Построить breadcrumbs
        breadcrumbs = [{'name': '🏠 Главная', 'url': '/'}]
        current_category = category
        while current_category:
            breadcrumbs.append({
                'name': current_category['name'].lower(),
                'url': f'/category/{current_category["id"]}',
            })
            if current_category.get('parent_id'):
                parent_category = await get_category(current_category['parent_id'])
                if parent_category:
                    current_category = parent_category
                else:
                    break
            else:
                break

        # Добавить название товара в конец breadcrumbs
        breadcrumbs.append({
            'name': product['name'],
            'url': f'/product/{product_id}',
        })

        return aioj.render_template("product_item.html", request, {
            "product": product,
            "breadcrumbs": breadcrumbs
        })
    
    except ValueError:
        return web.Response(text="Invalid product ID", status=400)
    except Exception as e:
        logger.error(f"Product handler error: {e}")
        return web.Response(text="Internal Server Error", status=500)


async def handle_category(request):
    """Страница категории с пагинацией."""
    try:
        category_id = int(request.match_info["category_id"])
        category = await get_category(category_id)

        if not category:
            return web.Response(text="Category not found", status=404)

        # Пагинация
        page = int(request.query.get('page', 1))
        per_page = 20

        # Получаем товары для текущей страницы
        products = await get_products_by_category(category_id, page, per_page)

        # Получаем общее количество товаров в категории
        total_products = await get_total_products_by_category(category_id)

        # Вычисляем общее количество страниц
        total_pages = (total_products + per_page - 1) // per_page if total_products else 1

        # Хлебные крошки
        breadcrumbs = [{'name': '🏠', 'url': '/'}]
        current_category = category
        while current_category and current_category.get('parent_id'):
            parent_category = await get_category(current_category['parent_id'])
            if parent_category:
                breadcrumbs.append({
                    'name': parent_category['name'].lower(),
                    'url': f'/category/{parent_category["id"]}',
                })
                current_category = parent_category
            else:
                break
        breadcrumbs.append({
            'name': category['name'].lower(),
            'url': f'/category/{category["id"]}',
        })

        # Контекст для шаблона
        context = {
            'category': category,
            'products': products,
            'breadcrumbs': breadcrumbs,
            'page': page,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_previous': page > 1,
        }

        return aioj.render_template("category.html", request, context)
    except Exception as e:
        logger.error(f"Error in handle_category: {e}", exc_info=True)
        return web.Response(text="Internal Server Error", status=500)


async def handle_search(request):
    """Обработчик поиска товаров."""
    query = request.query.get("q", "").strip()
    if not query:
        return web.HTTPFound("/")

    try:
        products = await database.fetch_all(
            """SELECT id, name, price, main_image as image
               FROM products_product
               WHERE name ILIKE $1""",
            f"%{query}%"
        )
        context = {"products": products, "query": query}
        return aioj.render_template("search.html", request, context)
    except Exception as e:
        logger.error(f"Error in handle_search: {e}")
        return web.Response(text="Internal Server Error", status=500)


async def handle_product(request):
    """Страница товара."""
    try:
        product_id = int(request.match_info["product_id"])
        if not await product_exists(product_id):
            return web.Response(text="Product not found", status=404)

        if (product := await get_product(product_id)) is None:
            return web.Response(text="Product not available", status=410)

        return aioj.render_template("product_item.html", request, {"product": product})
    
    except ValueError:
        return web.Response(text="Invalid product ID", status=400)
    except Exception as e:
        logger.error(f"Product handler error: {e}")
        return web.Response(text="Internal Server Error", status=500)
