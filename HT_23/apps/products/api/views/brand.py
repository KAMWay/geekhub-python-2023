from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
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

    @extend_schema(
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(description="Brand created successfully"),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Brand not created")
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
