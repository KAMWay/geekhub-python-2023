from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from apps.products.models import ScrapyTask
from apps.products.serializers import ScrapyTaskSerializer

from apps.products.api.tags import SCRAPY_TASK_TAG


@extend_schema(
    tags=[SCRAPY_TASK_TAG],
)
class ScrapyTaskViewSet(ModelViewSet):
    queryset = ScrapyTask.objects.all().order_by('id')
    serializer_class = ScrapyTaskSerializer
