from django.contrib import admin
from .models import TelegramUser, DeliveryAddress
from apps.cart.models import CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'total_cost', 'created_at', 'updated_at')
    
    def total_cost(self, obj):
        return obj.total_cost
    total_cost.short_description = 'Общая стоимость'


class DeliveryAddressInline(admin.TabularInline):
    model = DeliveryAddress
    extra = 0
    readonly_fields = ('country', 'city', 'street', 'building', 'postal_code', 'phone', 'is_primary')


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'username', 'first_name', 'last_name')
    search_fields = ('telegram_id', 'username', 'first_name', 'last_name')
    inlines = [CartItemInline, DeliveryAddressInline]


admin.site.register(TelegramUser, TelegramUserAdmin)
