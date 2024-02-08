from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from apps.accounts.serializers import UserSerializer

from apps.accounts.api_tags import USER_TAG


@extend_schema(
    tags=[USER_TAG],
)
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
