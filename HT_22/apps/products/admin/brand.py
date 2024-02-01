from django.contrib import admin

from apps.products.models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
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

