from django.urls import path
from django.urls import re_path

from . import views

app_name = "product"
urlpatterns = [
    path('', views.ProductListView.as_view(), name='index'),
    path("save/", views.SaveFormView.as_view(), name="save"),
    re_path(r'^(?P<pk>[A-Za-z][0-9]{9})/$', views.ProductDetailView.as_view(), name='detail'),
]
