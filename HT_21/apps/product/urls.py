from django.urls import path

from . import views

app_name = "product"
urlpatterns = [
    path("upload/", views.ProductUploadView.as_view(), name="upload"),
    path("update/<pk>/", views.ProductUpdateView.as_view(), name="update"),
    path("delete/<pk>/", views.ProductDeleteView.as_view(), name="delete"),
    path("detail/<pk>/", views.ProductDetailView.as_view(), name="detail"),
]
