import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from .models import Cart

# Create your views here.

logger = logging.getLogger('django')


class CartView(generic.ListView):
    model = Cart
    template_name = 'cart/index.html'
    context_object_name = 'cart_items'

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            return super().get(request, *args, **kwargs)
        else:
            messages.error(request, 'Please login to continue.')
            return redirect('account:login')

    def get_queryset(self):
        return Cart(self.request)

    def post(self, request, *args, **kwargs):
        if request.user and not request.user.is_authenticated:
            redirect('cart:index')

        product_id = request.POST.get('product_id')
        cart = Cart(request)
        if product_id:
            if cart.is_exist(product_id):
                upd_quantity = int(request.POST.get('product_quantity'))
                if upd_quantity == 0:
                    cart.delete(product_id)
                else:
                    product_quantity = cart.product_quantity(product_id)
                    if product_quantity + upd_quantity > 0:
                        cart.update(product_id, product_quantity + upd_quantity)
                    else:
                        messages.error(request, f'update product by id:{product_id} in cart unsuccessful')
        else:
            cart.clear()

        return redirect(reverse('cart:index'))
