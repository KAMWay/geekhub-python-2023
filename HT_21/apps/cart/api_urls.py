from django.urls import path

from cart.api_views import CartApiView

app_name = 'api_cart'
urlpatterns = [
    path('', CartApiView.as_view())
]
