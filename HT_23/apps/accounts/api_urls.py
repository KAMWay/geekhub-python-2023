from django.urls import path, include
from rest_framework import routers

from . import api_views

router = routers.DefaultRouter()
router.register(prefix=r'users', viewset=api_views.UserViewSet)
router.register(r'groups', api_views.GroupViewSet)

app_name = "api_accounts"
urlpatterns = [
    path("", include(router.urls)),
]
