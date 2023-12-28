from time import sleep

from django.shortcuts import render
from django.views import generic
from .forms import ProductForm
from .models import Product
from .tasks import ScrapingTask

import logging

logger = logging.getLogger(__name__)

# Create your views here.
class SaveFormView(generic.FormView):
    template_name = 'product/save.html'
    form_class = ProductForm

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST)
        context = {'form': ProductForm()}

        if form.is_valid():
            try:
                ids_str = form.cleaned_data['ids']
                ids = [item.strip() for item in ids_str.split(sep=',')]
                self.__scrap_task(ids)
                context.update({'message': 'Products scraping start successfully'})
            except Exception:
                context.update({'message': 'Products scraping start unsuccessfully'})
        else:
            context.update({'message': 'Form data unsuccessfully'})

        return render(request, 'product/save.html', context=context)

    def __scrap_task(self, ids: list):
        for id in ids:
            try:
                task = ScrapingTask()
                task.start(id)
                sleep(20)
            except Exception as e:
                logger.warning(f'Exception scraping {id}: {e}')
            else:
                logger.info(f'Scraping {id} done')


class ProductListView(generic.ListView):
    model = Product
    template_name = 'product/index.html'
    context_object_name = 'product_list'


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'product/detail.html'
    context_object_name = 'product'
