import logging
import subprocess
from sys import stdout, stdin, stderr

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import generic

from .forms import ProductForm
from .models import Product, Category
from ..cart.models import Cart

logger = logging.getLogger('django')


class SaveFormView(generic.FormView):
    template_name = 'product/save.html'
    form_class = ProductForm

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        else:
            messages.error(request, 'Not access')
            return redirect('index')

    def post(self, request, *args, **kwargs):
        if request.user and not request.user.is_superuser:
            redirect('product:save')

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
    CATEGORIES_KEY = 'categories'
    CATEGORY_CHOICES_KEY = 'select_categories'

    model = Product
    template_name = 'product/index.html'
    context_object_name = 'products'

    def post(self, request, *args, **kwargs):
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
                logger.error(f'added product by id:{product_id} to cart unsuccessful')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        categories = Category.objects.all()
        context[self.CATEGORIES_KEY] = categories

        select_categories = self.request.GET.getlist(self.CATEGORY_CHOICES_KEY)
        if len(select_categories) > 0:
            ids = list(map(int, select_categories))
            products = Product.objects.filter(categories__in=ids)
            context[self.context_object_name] = products
            context[self.CATEGORY_CHOICES_KEY] = ids
        # elif self.CATEGORY_CHOICES_KEY not in self.request.GET.keys():
        #     context[self.CATEGORY_CHOICES_KEY] = [category.id for category in categories]

        return context


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'product/detail.html'
    context_object_name = 'product'

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        else:
            messages.error(request, 'Not access')
            return redirect('index')
