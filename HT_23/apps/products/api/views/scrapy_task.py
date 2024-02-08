from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from apps.products.api.tags import SCRAPY_TASK_TAG
from apps.products.models import ScrapyTask
from apps.products.serializers import ScrapyTaskSerializer


@extend_schema(
    tags=[SCRAPY_TASK_TAG],
)
class ScrapyTaskViewSet(ModelViewSet):
    queryset = ScrapyTask.objects.all().order_by('id')
    serializer_class = ScrapyTaskSerializer
    permission_classes = [IsAdminUser]
