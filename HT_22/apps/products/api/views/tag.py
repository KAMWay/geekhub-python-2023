from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from apps.products.models import Tag
from apps.products.serializers import TagSerializer

from apps.products.api.tags import TAG_TAG


@extend_schema(
    tags=[TAG_TAG],
)
class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all().order_by('id')
    serializer_class = TagSerializer
