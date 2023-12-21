from django.contrib import admin

from product.models import Category
from product.models import Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", ]
    search_fields = ["name"]


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "description", "category", ]
    list_filter = ["category"]
    search_fields = ["name"]


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
