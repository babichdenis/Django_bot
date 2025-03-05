from django.contrib import admin
from .models import CartItem
from django.contrib.admin import SimpleListFilter

class TelegramIDFilter(SimpleListFilter):
    title = 'Telegram ID'
    parameter_name = 'telegram_id'

    def lookups(self, request, model_admin):
        users = set(CartItem.objects.values_list('user__telegram_id', flat=True))
        return [(user, str(user)) for user in users]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user__telegram_id=self.value())
        return queryset


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'get_product', 'quantity', 'total_cost', 'created_at', 'updated_at')
    list_filter = (TelegramIDFilter, 'created_at', 'updated_at')  # Добавляем кастомный фильтр
    search_fields = ('user__telegram_id', 'product__name')

    def get_user(self, obj):
        """Отображение пользователя."""
        return obj.user.username or obj.user.telegram_id
    get_user.short_description = 'Пользователь'

    def get_product(self, obj):
        """Отображение товара."""
        return obj.product.name
    get_product.short_description = 'Товар'

    def total_cost(self, obj):
        """Общая стоимость товара."""
        return f"{obj.quantity * obj.product.price} руб."
    total_cost.short_description = 'Общая стоимость'


admin.site.register(CartItem, CartItemAdmin)
