from django.contrib import admin

# from apps.core.models import DeliveryAddress, TelegramUser

# # users/admin.py


# class DeliveryAddressInline(admin.TabularInline):
#     model = DeliveryAddress
#     extra = 0
#     fields = (
#         'country',
#         'city',
#         'street',
#         'building',
#         'apartment',
#         'postal_code',
#         'phone',
#         'is_primary',
#         'is_active'
#     )
#     readonly_fields = ('created_at', 'updated_at')
#     show_change_link = True


# @admin.register(TelegramUser)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('telegram_id', 'username', 'addresses_count')
#     inlines = [DeliveryAddressInline]
#     readonly_fields = ('created_at', 'updated_at')
#     search_fields = ('telegram_id', 'username')

#     def addresses_count(self, obj):
#         return obj.addresses.count()
#     addresses_count.short_description = ('Количество адресов')


# @admin.register(DeliveryAddress)
# class DeliveryAddressAdmin(admin.ModelAdmin):
#     list_display = ('TelegramUser', 'short_address', 'is_primary', 'is_active')
#     list_filter = ('is_primary', 'is_active')
#     search_fields = ('user__telegram_id', 'city', 'street')

#     def short_address(self, obj):
#         return f"{obj.city}, {obj.street} {obj.building}"
#     short_address.short_description = ('Адрес')
