from django.urls import path, include
from rest_framework import routers

from . import api_views

router = routers.DefaultRouter()
router.register(prefix=r'categories', viewset=api_views.CategoryViewSet, basename='categories')
router.register(prefix=r'brands', viewset=api_views.BrandAPIView, basename='brands')
router.register(prefix=r'products', viewset=api_views.ProductViewSet, basename='products')
router.register(prefix=r'scrapy_tasks', viewset=api_views.ScrapyTaskViewSet, basename='scrapy_tasks')
router.register(prefix=r'tags', viewset=api_views.TagViewSet, basename='tags')

app_name = "api_account"
urlpatterns = [
    path("", include(router.urls)),
]
