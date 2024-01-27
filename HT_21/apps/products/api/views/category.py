from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from apps.products.models import Category
from apps.products.serializers import CategorySerializer

from apps.products.api.tags import CATEGORY_TAG


@extend_schema(
    tags=[CATEGORY_TAG],
)
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
