from rest_framework.viewsets import ModelViewSet

from apps.products.models import Tag
from apps.products.serializers import TagSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all().order_by('id')
    serializer_class = TagSerializer
