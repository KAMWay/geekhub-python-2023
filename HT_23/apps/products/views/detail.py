from django.views.generic import DetailView

from apps.products.models import Product


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
