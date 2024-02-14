import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from apps.products.models import Product

logger = logging.getLogger('django')


class ProductDeleteView(generic.DeleteView):
    model = Product
    success_url = reverse_lazy("index")

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        else:
            messages.error(request, 'Not access for delete')
            return redirect('index')

    def post(self, request, *args, **kwargs):
        if request.user and not request.user.is_superuser:
            redirect('products:update')

        return super().post(request, *args, **kwargs)
