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
      │  │  ├─ base.css
      │  │  ├─ changelists.css
      │  │  ├─ dark_mode.css
      │  │  ├─ dashboard.css
      │  │  ├─ forms.css
      │  │  ├─ login.css
      │  │  ├─ nav_sidebar.css
      │  │  ├─ responsive.css
      │  │  ├─ responsive_rtl.css
      │  │  ├─ rtl.css
      │  │  ├─ unusable_password_field.css
      │  │  ├─ vendor
      │  │  │  └─ select2
      │  │  │     ├─ LICENSE-SELECT2.md
      │  │  │     ├─ select2.css
      │  │  │     └─ select2.min.css
      │  │  └─ widgets.css
      │  ├─ img
      │  │  ├─ LICENSE
      │  │  ├─ README.txt
      │  │  ├─ calendar-icons.svg
      │  │  ├─ gis
      │  │  │  ├─ move_vertex_off.svg
      │  │  │  └─ move_vertex_on.svg
      │  │  ├─ icon-addlink.svg
      │  │  ├─ icon-alert.svg
      │  │  ├─ icon-calendar.svg
      │  │  ├─ icon-changelink.svg
      │  │  ├─ icon-clock.svg
      │  │  ├─ icon-deletelink.svg
      │  │  ├─ icon-hidelink.svg
      │  │  ├─ icon-no.svg
      │  │  ├─ icon-unknown-alt.svg
      │  │  ├─ icon-unknown.svg
      │  │  ├─ icon-viewlink.svg
      │  │  ├─ icon-yes.svg
      │  │  ├─ inline-delete.svg
      │  │  ├─ search.svg
      │  │  ├─ selector-icons.svg
      │  │  ├─ sorting-icons.svg
      │  │  ├─ tooltag-add.svg
      │  │  └─ tooltag-arrowright.svg
      │  └─ js
      │     ├─ SelectBox.js
      │     ├─ SelectFilter2.js
      │     ├─ actions.js
      │     ├─ admin
      │     │  ├─ DateTimeShortcuts.js
      │     │  └─ RelatedObjectLookups.js
      │     ├─ autocomplete.js
      │     ├─ calendar.js
      │     ├─ cancel.js
      │     ├─ change_form.js
      │     ├─ core.js
      │     ├─ filters.js
      │     ├─ inlines.js
      │     ├─ jquery.init.js
      │     ├─ nav_sidebar.js
      │     ├─ popup_response.js
      │     ├─ prepopulate.js
      │     ├─ prepopulate_init.js
      │     ├─ theme.js
      │     ├─ unusable_password_field.js
      │     ├─ urlify.js
      │     └─ vendor
      │        ├─ jquery
      │        │  ├─ LICENSE.txt
      │        │  ├─ jquery.js
      │        │  └─ jquery.min.js
      │        ├─ select2
      │        │  ├─ LICENSE.md
      │        │  ├─ i18n
      │        │  │  ├─ af.js
      │        │  │  ├─ ar.js
      │        │  │  ├─ az.js
      │        │  │  ├─ bg.js
      │        │  │  ├─ bn.js
      │        │  │  ├─ bs.js
      │        │  │  ├─ ca.js
      │        │  │  ├─ cs.js
      │        │  │  ├─ da.js
      │        │  │  ├─ de.js
      │        │  │  ├─ dsb.js
      │        │  │  ├─ el.js
      │        │  │  ├─ en.js
      │        │  │  ├─ es.js
      │        │  │  ├─ et.js
      │        │  │  ├─ eu.js
      │        │  │  ├─ fa.js
      │        │  │  ├─ fi.js
      │        │  │  ├─ fr.js
      │        │  │  ├─ gl.js
      │        │  │  ├─ he.js
      │        │  │  ├─ hi.js
      │        │  │  ├─ hr.js
      │        │  │  ├─ hsb.js
      │        │  │  ├─ hu.js
      │        │  │  ├─ hy.js
      │        │  │  ├─ id.js
      │        │  │  ├─ is.js
      │        │  │  ├─ it.js
      │        │  │  ├─ ja.js
      │        │  │  ├─ ka.js
      │        │  │  ├─ km.js
      │        │  │  ├─ ko.js
      │        │  │  ├─ lt.js
      │        │  │  ├─ lv.js
      │        │  │  ├─ mk.js
      │        │  │  ├─ ms.js
      │        │  │  ├─ nb.js
      │        │  │  ├─ ne.js
      │        │  │  ├─ nl.js
      │        │  │  ├─ pl.js
      │        │  │  ├─ ps.js
      │        │  │  ├─ pt-BR.js
      │        │  │  ├─ pt.js
      │        │  │  ├─ ro.js
      │        │  │  ├─ ru.js
      │        │  │  ├─ sk.js
      │        │  │  ├─ sl.js
      │        │  │  ├─ sq.js
      │        │  │  ├─ sr-Cyrl.js
      │        │  │  ├─ sr.js
      │        │  │  ├─ sv.js
      │        │  │  ├─ th.js
      │        │  │  ├─ tk.js
      │        │  │  ├─ tr.js
      │        │  │  ├─ uk.js
      │        │  │  ├─ vi.js
      │        │  │  ├─ zh-CN.js
      │        │  │  └─ zh-TW.js
      │        │  ├─ select2.full.js
      │        │  └─ select2.full.min.js
      │        └─ xregexp
      │           ├─ LICENSE.txt
      │           ├─ xregexp.js
      │           └─ xregexp.min.js
      └─ main
         ├─ css
         │  └─ style.css
         └─ js
            └─ cart.js

```