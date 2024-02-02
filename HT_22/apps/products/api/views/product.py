import logging
import subprocess
import sys

from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.products.api.permissions import DefaultPermission
from apps.products.api.tags import PRODUCT_TAG
from apps.products.models import Product, ScrapyTask
from apps.products.serializers import ProductSerializer

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
            status.HTTP_201_CREATED: OpenApiResponse(
                description='Scraping task run successfully',
                response=None,
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Exception run scraping task',
                response=None,
            ),
        },
        methods=["POST"]
    )
    def create(self, request, *args, **kwargs):
        if request.method.upper() != 'POST':
            return super().create(request, *args, **kwargs)

        ids_str = ''.join(ch for ch in str(dict(request.data).get('id')) if ch not in '"\'[]')
        task = ScrapyTask.objects.create(ids_str=ids_str)
        try:
            sys_execute = sys.executable
            subprocess.Popen([
                sys_execute,
                'manage.py',
                'scrape',
                str(task.id)
            ])
            logger.info(f'scraping subprocess by id:{task.id} run successful')
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            logger.error(f'scraping subprocess by id:{task.id} run unsuccessful')
            return Response(status=status.HTTP_400_BAD_REQUEST)
