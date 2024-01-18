from django.urls import path

from . import views

app_name = "product"
urlpatterns = [
    path("save/", views.SaveFormView.as_view(), name="save"),
    path("detail/<pk>/", views.ProductDetailView.as_view(), name="detail"),
]
