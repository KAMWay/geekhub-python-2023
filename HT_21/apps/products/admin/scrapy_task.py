from django.contrib import admin

from products.models import ScrapyTask


@admin.register(ScrapyTask)
class ScrapyTaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ids_str'
    )
    list_display_links = (
        'id',
    )
    ordering = (
        'id',
    )
