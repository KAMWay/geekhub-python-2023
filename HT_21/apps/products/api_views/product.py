from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from apps.products.models import Product
from apps.products.serializers import ProductSerializer
from apps.products.api_tags import PRODUCT_TAG


@extend_schema(
    tags=[PRODUCT_TAG],
)
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
