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
    get_top_level_categories,
    get_subcategories
)
from utils.logger import logger
from utils.utils import handle_errors


# Функция для построения breadcrumbs
async def get_breadcrumbs(category_id: int = None, product_id: int = None):
    """Получить breadcrumbs для категории или товара с учетом подкатегорий."""
    breadcrumbs = [{'name': 'Главная', 'url': '/'}]

    if category_id:
        current_id = category_id
    elif product_id:
        product = await get_product(product_id)
        if not product:
            return breadcrumbs
        current_id = product['category_id']
    else:
        return breadcrumbs

    all_categories = await get_categories()
    categories_dict = {cat['id']: cat for cat in all_categories}

    # Собираем breadcrumbs для родительских категорий
    while current_id:
        category = categories_dict.get(current_id)
        if not category:
            break

        breadcrumbs.append({
            'name': category.get('name', 'Без названия'),
            'url': f"/category/{category['id']}"
        })

        current_id = category.get('parent_id')

    # Добавляем текущую страницу (без ссылки)
    if category_id:
        current_category = categories_dict.get(category_id)
        if current_category:
            breadcrumbs.append({
                'name': current_category.get('name', 'Без названия'),
                'url': None
            })
    elif product_id:
        breadcrumbs.append({
            'name': product['name'],
            'url': None
        })

    return breadcrumbs


@handle_errors
async def handle_index(request):
    """Главная страница с популярными товарами и категориями."""
    context = {
        "featured_products": await get_featured_products(),
        "categories": await get_top_level_categories(),
    }
    return aioj.render_template("index.html", request, context)


@handle_errors
async def handle_category(request):
    """Страница категории с пагинацией."""
    category_id = int(request.match_info["category_id"])
    category = await get_category(category_id)
    if not category:
        return web.Response(text="Category not found", status=404)

    subcategories = await get_subcategories(category_id)
    breadcrumbs = await get_breadcrumbs(category_id=category_id)

    page = int(request.query.get('page', 1))
    per_page = 20
    products = await get_products_by_category(category_id, page, per_page)
    total_products = await get_total_products_by_category(category_id)
    total_pages = (total_products + per_page -
                   1) // per_page if total_products else 1

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


@handle_errors
async def handle_product(request):
    """Страница товара."""
    product_id = int(request.match_info["product_id"])
    if not await product_exists(product_id):
        return web.Response(text="Product not found", status=404)

    product = await get_product(product_id)
    breadcrumbs = await get_breadcrumbs(product_id=product_id)

    return aioj.render_template("product_item.html", request, {
        "product": product,
        "breadcrumbs": breadcrumbs
    })
