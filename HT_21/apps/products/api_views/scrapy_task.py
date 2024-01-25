from rest_framework.viewsets import ModelViewSet

from apps.products.models import ScrapyTask
from apps.products.serializers import ScrapyTaskSerializer


class ScrapyTaskViewSet(ModelViewSet):
    queryset = ScrapyTask.objects.all().order_by('id')
    serializer_class = ScrapyTaskSerializer
