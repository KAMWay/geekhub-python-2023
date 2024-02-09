import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import FormView

from apps.products.forms import ProductForm
from apps.tasks import scraping_items

logger = logging.getLogger('django')


class ProductUploadView(FormView):
    template_name = 'products/upload.html'
    form_class = ProductForm

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        else:
            messages.error(request, 'Not access')
            return redirect('index')

    def post(self, request, *args, **kwargs):
        if request.user and request.user.is_superuser:
            form = ProductForm(request.POST)
            if form.is_valid():
                ids_str = form.cleaned_data['ids']
                ids = ids_str.split(',')
                scraping_items.delay(ids=ids)
                messages.info(request, 'Products send to scraping successfully')
            else:
                messages.error(request, 'Form data unsuccessfully')

        redirect_url = request.GET.get('next')
        if redirect_url:
            return redirect(redirect_url)
        else:
            return redirect('products:upload')
