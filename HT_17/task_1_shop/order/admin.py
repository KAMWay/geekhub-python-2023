from django.contrib import admin

from order.models import Order
from order.models import Item


class ItemInline(admin.TabularInline):
    model = Item
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Base information", {"fields": ["order_date", "order_amount"]}),
    ]
    inlines = [ItemInline]
    list_display = ["info", "order_date", "order_amount"]
    list_filter = ["order_date"]


class ItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "product_quantity"]
    list_filter = ["order", "product"]


# Register your models here.
admin.site.register(Order, OrderAdmin)
admin.site.register(Item, ItemAdmin)
