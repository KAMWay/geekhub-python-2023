from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from apps.products.api.permissions import DefaultPermission
from apps.products.api.tags import BRAND_TAG
from apps.products.models import Brand
from apps.products.serializers import BrandSerializer


@extend_schema(
    tags=[BRAND_TAG],
)
class BrandAPIView(ModelViewSet):
    queryset = Brand.objects.all().order_by('id')
    serializer_class = BrandSerializer
    permission_classes = [DefaultPermission]
