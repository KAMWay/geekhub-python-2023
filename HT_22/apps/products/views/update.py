import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from apps.products.models import Product

logger = logging.getLogger('django')


class ProductUpdateView(UpdateView):
    model = Product
    fields = [
        'brand',
        'name',
        'main_image_url',
        'url',
        'regular_price',
        'sale_price',
        'default_seller_id',
        'store_id',
        'description',
        'category',
    ]
    template_name = 'products/update.html'
    success_url = reverse_lazy("index")

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        else:
            messages.error(request, 'Not access for update')
            return redirect('index')

    def get_success_url(self):
        redirect_url = self.request.GET.get('next')
        if redirect_url:
            self.success_url = redirect_url
        messages.info(self.request, 'Update success')

        return super().get_success_url()

    def post(self, request, *args, **kwargs):
        if request.user and not request.user.is_superuser:
            return redirect('products:update')

        return super().post(request, *args, **kwargs)
