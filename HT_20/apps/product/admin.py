from django.contrib import admin

from .models import Category
from .models import Product
from .models import Tag
from .models import ScrapyTask

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(ScrapyTask)
