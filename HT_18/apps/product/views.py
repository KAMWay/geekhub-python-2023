import logging
from concurrent.futures.thread import ThreadPoolExecutor

from django.shortcuts import render
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from .forms import ProductForm
from .models import Product
from .tasks import create_task

logger = logging.getLogger('django')
executor = ThreadPoolExecutor(max_workers=1)


class SaveFormView(generic.FormView):
    template_name = 'product/save.html'
    form_class = ProductForm

    # @csrf_exempt
    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST)
        context = {'form': ProductForm()}

        if form.is_valid():
            ids_str = form.cleaned_data['ids']
            ids = (item.strip() for item in ids_str.split(sep=','))
            try:
                # task = create_task.delay(list(set(ids)))
                task = create_task(list(set(ids)))
            except Exception as e:
                print(f'{e}')

            context.update({'message': f'Products scraping start successfully'})
        else:
            context.update({'message': 'Form data unsuccessfully'})

        return render(request, 'product/save.html', context=context)


class ProductListView(generic.ListView):
    model = Product
    template_name = 'product/index.html'
    context_object_name = 'product_list'


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'product/detail.html'
    context_object_name = 'product'
