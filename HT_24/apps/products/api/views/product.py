import logging

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.products.api.permissions import DefaultPermission
from apps.products.api.tags import PRODUCT_TAG
from apps.products.models import Product
from apps.products.serializers import ProductSerializer
from apps.tasks import scraping_items

logger = logging.getLogger('django')


@extend_schema(
    tags=[PRODUCT_TAG],
)
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [DefaultPermission]

    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description='Task for scraping products by IDs run successfully',
                response=None,
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Exception run task of scraping',
                response=None,
            ),
        },
        methods=["POST"],
        examples=[
            OpenApiExample(
                'Example Value',
                value={
                    "ids": "string of ids separated by comma"
                },
            ),
        ],
    )
    def create(self, request, *args, **kwargs):
        if request.method.upper() != 'POST':
            return super().create(request, *args, **kwargs)

        try:
            ids_str = ''.join(ch for ch in str(dict(request.data).get('ids')) if ch not in '"\'[]')
            ids = [item.strip() for item in ids_str.split(',')]
            scraping_items.apply_async(ids=ids)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            logger.error(f"scraping process run unsuccessful")
            return Response(status=status.HTTP_400_BAD_REQUEST)
