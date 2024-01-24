from django.contrib.auth import views as auth_views
from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(prefix=r'users', viewset=views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

app_name = "accounts"
urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
