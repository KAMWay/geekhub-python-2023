import logging
import subprocess
from sys import stdout, stdin, stderr

from django.shortcuts import render
from django.views import generic

from .forms import ProductForm
from .models import Product

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

        return render(request, 'product/save.html', context=context)

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


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'product/detail.html'
    context_object_name = 'product'
