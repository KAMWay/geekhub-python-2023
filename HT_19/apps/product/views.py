import logging
import subprocess
from sys import stdout, stdin, stderr

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from .forms import ProductForm
from .models import Product, Cart

logger = logging.getLogger('django')


class SaveFormView(generic.FormView):
    template_name = 'product/save.html'
    form_class = ProductForm

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST)
        context = {'form': ProductForm()}

        if form.is_valid():
            ids_str = form.cleaned_data['ids']
            ids = set(item.strip() for item in ids_str.split(sep=','))
            self.__run_subprocess(ids)
            context.update({'message': 'Products scraping start successfully'})
        else:
            context.update({'message': 'Form data unsuccessfully'})

        return render(request, self.template_name, context=context)

    def __run_subprocess(self, ids: set):
        try:
            command = f'python manage.py shell --command="from apps.product.tasks import ScrapingTask; ScrapingTask({ids}).run()"'
            process = subprocess.Popen(command, shell=True, stdin=stdin, stdout=stdout, stderr=stderr)
            logger.info(f'subprocess id:{process.pid} run successful')
        except Exception:
            logger.error(f'subprocess run unsuccessful')


class ProductListView(generic.ListView):
    model = Product
    template_name = 'product/index.html'
    context_object_name = 'product_list'

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        product_id = request.GET.get('product_id')
        if product_id:
            if cart.is_exist(product_id):
                cart.delete(product_id)
            else:
                try:
                    product_quantity = int(request.GET.get('product_quantity'))
                    if product_quantity > 0:
                        cart.update(product_id, product_quantity)
                    else:
                        raise Exception
                except Exception:
                    logger.error(f'added product by id:{product_id} to cart unsuccessful')

            return redirect(reverse('product:index'))

        return super().get(request)


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'product/detail.html'
    context_object_name = 'product'


class CartView(generic.ListView):
    model = Cart
    template_name = 'product/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return Cart(self.request)

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        cart = Cart(request)
        if product_id:
            try:
                if cart.is_exist(product_id):
                    upd_quantity = int(request.POST.get('product_quantity'))
                    if upd_quantity == 0:
                        cart.delete(product_id)
                    else:
                        product_quantity = cart.product_quantity(product_id)
                        if product_quantity + upd_quantity > 0:
                            cart.update(product_id, product_quantity + upd_quantity)
                        else:
                            raise Exception
            except Exception:
                logger.error(f'update product by id:{product_id} in cart unsuccessful')
        else:
            cart.clear()

        return redirect(reverse('product:cart'))
