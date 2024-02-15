from django.urls import path, include
from rest_framework import routers

from apps.products.api import views

router = routers.DefaultRouter()
router.register(prefix=r'categories', viewset=views.CategoryViewSet, basename='categories')
router.register(prefix=r'brands', viewset=views.BrandAPIView, basename='brands')
router.register(prefix=r'products', viewset=views.ProductViewSet, basename='products')
router.register(prefix=r'tags', viewset=views.TagViewSet, basename='tags')

app_name = "api_products"
urlpatterns = [
    path("", include(router.urls)),
]
