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
                product_quantity = int(request.GET.get('product_quantity')) or 1
                cart.update(product_id, product_quantity if product_quantity > 0 else 1)

            return redirect(reverse('product:index'))
        print(len(cart))
        [print(item) for item in cart]

        return super().get(request)

    def valida(self):
        ...


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'product/detail.html'
    context_object_name = 'product'
