from django.contrib import admin
from .models import Category, Product


class ProductInline(admin.TabularInline):
    model = Product.categories.through  # Используем промежуточную модель
    extra = 1  # Количество пустых форм для добавления продуктов
    verbose_name = 'Продукт'
    verbose_name_plural = 'Продукты'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'product':
            kwargs['queryset'] = Product.objects.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Поля, которые будут отображаться в списке
    list_display = ('name', 'parent', 'slug', 'is_active')
    list_filter = ('is_active', 'parent')  # Фильтры в правой части админки
    search_fields = ('name', 'slug')  # Поиск по названию и slug
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')  # Поля только для чтения

    # Дополнительные действия в админке
    actions = ['make_active', 'make_inactive']
    inlines = [ProductInline]

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Активировать выбранные категории"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Деактивировать выбранные категории"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'stock',
                    'available', 'stock_status')  # Поля в списке
    list_filter = ('available', 'categories')  # Фильтры
    search_fields = ('name', 'sku', 'description')  # Поиск
    filter_horizontal = ('categories',)  # Удобный выбор категорий
    readonly_fields = ('created_at', 'updated_at',
                       'stock_status')  # Поля только для чтения

    # Дополнительные действия в админке
    actions = ['make_available', 'make_unavailable']

    def stock_status(self, obj):
        return obj.stock_status
    stock_status.short_description = 'Статус остатка'

    def make_available(self, request, queryset):
        queryset.update(available=True)
    make_available.short_description = "Сделать выбранные товары доступными"

    def make_unavailable(self, request, queryset):
        queryset.update(available=False)
    make_unavailable.short_description = "Сделать выбранные товары недоступными"
