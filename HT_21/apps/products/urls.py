from django.urls import path

from . import views

app_name = "products"
urlpatterns = [
    path("upload/", views.ProductUploadView.as_view(), name="upload"),
    path("update/<pk>/", views.ProductUpdateView.as_view(), name="update"),
    path("delete/<pk>/", views.ProductDeleteView.as_view(), name="delete"),
    path("<pk>/", views.ProductDetailView.as_view(), name="detail"),
]
