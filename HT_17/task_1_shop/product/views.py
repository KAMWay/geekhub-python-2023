import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Category

from .models import Product


# Create your views here.
def product_index(request):
    product_list = Product.objects.all().values()
    json_data = json.dumps(list(product_list), cls=DjangoJSONEncoder)
    return HttpResponse(json_data, content_type='application/json')


def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        json_data = json.dumps(product.to_dict(), cls=DjangoJSONEncoder)
        return HttpResponse(json_data, content_type='application/json')
    except Product.DoesNotExist:
        raise Http404("Product does not exist")


def category_index(request):
    category_list = Category.objects.all().values()
    json_data = json.dumps(list(category_list), cls=DjangoJSONEncoder)
    return HttpResponse(json_data, content_type='application/json')


def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    json_data = json.dumps(category.to_dict(), cls=DjangoJSONEncoder)
    return HttpResponse(json_data, content_type='application/json')
