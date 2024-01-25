from rest_framework.viewsets import ModelViewSet

from apps.products.models import Brand
from apps.products.serializers import BrandSerializer


class BrandAPIView(ModelViewSet):
    queryset = Brand.objects.all().order_by('id')
    serializer_class = BrandSerializer
