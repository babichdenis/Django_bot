from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.html import format_html
from .models import Order, OrderItem, OrderStatusHistory
from apps.core.models import DeliveryAddress

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    list_display = ('id', 'user', 'status', 'payment_status', 'total')
    list_filter = ('status', 'payment_status')
    search_fields = ('id', 'user__telegram_id')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')
    list_filter = ('order__status',)

class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'status')
    list_filter = ('order__status',)

class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'country', 'city', 'street')
    list_filter = ('user', 'is_primary')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderStatusHistory, OrderStatusHistoryAdmin)
admin.site.register(DeliveryAddress, DeliveryAddressAdmin)
