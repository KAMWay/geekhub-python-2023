from django.contrib import admin

from apps.products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name'
    )
    list_display_links = (
        'id',
    )
    ordering = (
        'id',
    )
