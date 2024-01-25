import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView

from apps.cart.models import Cart
from apps.products.models import Product, Category

logger = logging.getLogger('django')


class ProductListView(ListView):
    CATEGORIES_KEY = 'categories'
    CATEGORY_CHOICES_KEY = 'select_categories'

    model = Product
    template_name = 'products/index.html'
    context_object_name = 'products'

    def post(self, request, *args, **kwargs):
        if request.user and not request.user.is_authenticated:
            messages.error(request, 'Not access')
            return redirect('index')

        product_id = request.POST.get('product_id')
        if product_id:
            product_quantity = int(request.POST.get('product_quantity'))
            cart = Cart(request)
            self.__product_to_cart(product_id, product_quantity, cart)

        return redirect('index')

    def __product_to_cart(self, product_id: str, product_quantity: int, cart: Cart):
        if cart.is_exist(product_id):
            cart.delete(product_id)
        else:
            try:
                if product_quantity > 0:
                    cart.update(product_id, product_quantity)
                else:
                    raise Exception
            except Exception:
                logger.error(f'added products by id:{product_id} to cart unsuccessful')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        categories = Category.objects.all()
        context[self.CATEGORIES_KEY] = categories

        select_categories = self.request.GET.getlist(self.CATEGORY_CHOICES_KEY)
        if len(select_categories) > 0:
            ids = list(map(int, select_categories))
            products = Product.objects.filter(category__in=ids)
            context[self.context_object_name] = products
            context[self.CATEGORY_CHOICES_KEY] = ids

        return context
