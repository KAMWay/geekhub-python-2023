from django.urls import path

from . import views

app_name = "product"
urlpatterns = [
    path('', views.ProductListView.as_view(), name='index'),
    path("save/", views.SaveFormView.as_view(), name="save"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("detail/<pk>/", views.ProductDetailView.as_view(), name="detail"),
]
