from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        # (None, {"fields": ["brand_name"]}),
        (None, {'fields': ['id', 'brand_name', 'name', 'main_image_url', 'url', 'regular_price', 'sale_price',
                           'default_seller_id', 'store_id', ]}),
        # ("Description", {"fields": ["description"]}),
        ('Description', {'fields': ['description'], 'classes': ['collapse']}),
    ]
    list_display = ["id", "name", 'regular_price', 'sale_price']


# Register your models here.
admin.site.register(Product, ProductAdmin)
