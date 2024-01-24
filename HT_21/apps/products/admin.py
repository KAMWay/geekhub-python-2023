from django.contrib import admin

from .models import Category, Brand
from .models import Product
from .models import Tag
from .models import ScrapyTask

# Register your models here.
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ScrapyTask)
admin.site.register(Tag)
