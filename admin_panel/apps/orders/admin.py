from django.contrib import admin
# from apps.orders.models import Order


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('TelegramUser', 'address_short', 'total', 'status', 'is_active')
#     list_filter = ('status', 'is_active')
#     search_fields = ('user__telegram_id', 'address__city', 'address__street')
#     readonly_fields = ('created_at', 'updated_at')

#     def address_short(self, obj):
#         return f"{obj.address.city}, {obj.address.street} {obj.address.building}"
#     address_short.short_description = ('Адрес')

#     actions = ['cancel_orders']

#     def cancel_orders(self, request, queryset):
#         queryset.update(status='canceled')
#     cancel_orders.short_description = ('Отменить выбранные заказы')
