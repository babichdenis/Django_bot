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
    get_total_products_by_category,
    get_top_level_categories  # Импортируем новую функцию
)
from utils.logger import logger
from utils.utils import handle_error
from database.db import database


async def handle_index(request):
    """Главная страница с популярными товарами и категориями."""
    try:
        context = {
            "featured_products": await get_featured_products(),
            "categories": await get_top_level_categories(),
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
        subcategories = await get_subcategories(category_id)
        breadcrumbs = await get_breadcrumbs(category_id)
        
        if not category:
            return web.Response(text="Category not found", status=404)

        # Получаем товары
        page = int(request.query.get('page', 1))
        per_page = 20
        products = await get_products_by_category(category_id, page, per_page)
        print(products)
        total_products = await get_total_products_by_category(category_id)
        total_pages = (total_products + per_page - 1) // per_page if total_products else 1

        # Контекст для шаблона
        context = {
            'category': category,
            'subcategories': subcategories,
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


async def get_all_categories():
    """Получить все категории."""
    query = "SELECT id, name, parent_id FROM products_category"
    return await database.fetch_all(query)

async def get_breadcrumbs(category_id: int):
    """Получить breadcrumbs для категории."""
    all_categories = await get_all_categories()
    categories_dict = {cat['id']: cat for cat in all_categories}  # Словарь для быстрого доступа

    breadcrumbs = []
    current_id = category_id

    while current_id:
        category = categories_dict.get(current_id)
        if not category:
            break  # Если категория не найдена, выходим из цикла

        breadcrumbs.append({
            'name': category.get('name', 'Без названия'),
            'url': f"/category/{category['id']}"
        })

        current_id = category.get('parent_id')

    # Добавляем корневую категорию (главную страницу)
    breadcrumbs.append({
        'name': '🏠 ',
        'url': '/'
    })

    # Разворачиваем список, чтобы начать с корневой категории
    breadcrumbs.reverse()
    return breadcrumbs


async def get_subcategories(parent_id: int):
    """Получить подкатегории по parent_id."""
    query = "SELECT id, name, image FROM products_category WHERE parent_id = $1"
    return await database.fetch_all(query, parent_id)
