from django.contrib import admin

from apps.products.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
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
