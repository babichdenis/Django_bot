# Django_bot

```
Django_bot
├─ .DS_Store
├─ .qodo
├─ README.md
├─ admin_panel
│  ├─ __init__.py
│  ├─ admin_panel
│  │  ├─ __init__.py
│  │  ├─ asgi.py
│  │  ├─ settings.py
│  │  ├─ urls.py
│  │  └─ wsgi.py
│  ├─ apps
│  │  ├─ __init__.py
│  │  ├─ cart
│  │  │  ├─ __init__.py
│  │  │  ├─ admin.py
│  │  │  ├─ apps.py
│  │  │  ├─ migrations
│  │  │  │  ├─ 0001_initial.py
│  │  │  │  └─ __init__.py
│  │  │  └─ models.py
│  │  ├─ core
│  │  │  ├─ __init__.py
│  │  │  ├─ admin.py
│  │  │  ├─ apps.py
│  │  │  ├─ migrations
│  │  │  │  ├─ 0001_initial.py
│  │  │  │  └─ __init__.py
│  │  │  ├─ models.py
│  │  │  └─ validators.py
│  │  ├─ orders
│  │  │  ├─ __init__.py
│  │  │  ├─ admin.py
│  │  │  ├─ apps.py
│  │  │  ├─ migrations
│  │  │  │  ├─ 0001_initial.py
│  │  │  │  ├─ 0002_alter_order_address.py
│  │  │  │  └─ __init__.py
│  │  │  ├─ models.py
│  │  │  └─ signals.py
│  │  ├─ payments
│  │  │  ├─ __init__.py
│  │  │  ├─ admin.py
│  │  │  ├─ apps.py
│  │  │  ├─ migrations
│  │  │  │  ├─ 0001_initial.py
│  │  │  │  ├─ 0002_alter_payment_payment_method.py
│  │  │  │  └─ __init__.py
│  │  │  ├─ models.py
│  │  │  └─ signals.py
│  │  └─ products
│  │     ├─ __init__.py
│  │     ├─ admin.py
│  │     ├─ apps.py
│  │     ├─ migrations
│  │     │  ├─ 0001_initial.py
│  │     │  └─ __init__.py
│  │     └─ models.py
│  ├─ dockerfile
│  ├─ manage.py
│  └─ requirements.txt
├─ bot_project
│  ├─ .DS_Store
│  ├─ Dockerfile
│  ├─ database
│  │  ├─ __init__.py
│  │  ├─ db.py
│  │  ├─ queries.py
│  │  ├─ queries_cart.py
│  │  └─ queries_orders.py
│  ├─ handlers
│  │  ├─ __init__.py
│  │  ├─ telegram_handlers.py
│  │  ├─ web_handler_cart.py
│  │  ├─ web_handlers.py
│  │  └─ web_handlers_orders.py
│  ├─ main.py
│  ├─ media
│  ├─ requirements.txt
│  ├─ routes
│  │  ├─ __init__.py
│  │  ├─ telegram.py
│  │  └─ web.py
│  ├─ templates
│  │  ├─ base.html
│  │  ├─ base_old.html
│  │  ├─ cart.html
│  │  ├─ category.html
│  │  ├─ includes
│  │  │  ├─ footer.html
│  │  │  └─ header.html
│  │  ├─ index.html
│  │  ├─ order_checkout.html
│  │  ├─ order_details.html
│  │  ├─ payment_result.py
│  │  ├─ product_item.html
│  │  └─ search.html
│  └─ utils
│     ├─ __init__.py
│     ├─ logger.py
│     └─ utils.py
├─ docker-compose.yml
├─ env_ex
└─ media
   ├─ categories
   │  ├─ img-pro-01.jpg
   │  ├─ img-pro-01_HJdKt9q.jpg
   │  ├─ img-pro-02.jpg
   │  ├─ img-pro-02_jXsFgr6.jpg
   │  ├─ img-pro-03.jpg
   │  ├─ img-pro-03_MOpPxsu.jpg
   │  ├─ img-pro-03_oqSFKcU.jpg
   │  └─ img-pro-04.jpg
   ├─ logo.png
   ├─ products
   │  ├─ product-ad-10.jpg
   │  ├─ product-cp-06.jpg
   │  ├─ product-cp-06_GIqcl4U.jpg
   │  ├─ product-cp-08.jpg
   │  ├─ product-dc-01.jpg
   │  ├─ product-dc-02.jpg
   │  ├─ product-dc-02_SHmxQjX.jpg
   │  ├─ product-dc-03.jpg
   │  ├─ product-dc-04.jpg
   │  └─ product-mb-15.jpg
   └─ static
      ├─ admin
      │  ├─ css
      │  │  ├─ autocomplete.css
 
      └─ main
         ├─ css
         │  └─ style.css
         └─ js
            └─ cart.js

```
