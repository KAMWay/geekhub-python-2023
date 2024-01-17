from django.contrib.auth import logout
from django.urls import path

from . import views

app_name = "account"
urlpatterns = [
    path("login/", views.AccountLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
]
