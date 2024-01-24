from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(prefix=r'users', viewset=views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

api = [
    path("api/", include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

app_name = "account"
urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]

urlpatterns += api
