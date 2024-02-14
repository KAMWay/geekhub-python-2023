from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from apps.products.api.permissions import DefaultPermission
from apps.products.api.tags import CATEGORY_TAG
from apps.products.models import Category
from apps.products.serializers import CategorySerializer


@extend_schema(
    tags=[CATEGORY_TAG],
)
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [DefaultPermission]
