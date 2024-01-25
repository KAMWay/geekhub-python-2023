from django.contrib import admin

from products.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
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
