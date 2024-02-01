from django.urls import path

from apps.cart.api.views import CartApiView

app_name = 'api_cart'
urlpatterns = [
    path('', CartApiView.as_view(), name='cart')
]
