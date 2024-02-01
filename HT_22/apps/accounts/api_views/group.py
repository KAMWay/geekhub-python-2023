from django.contrib.auth.models import Group
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions

from apps.accounts.serializers import GroupSerializer

from apps.accounts.api_tags import GROUP_TAG


@extend_schema(
    tags=[GROUP_TAG],
)
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
