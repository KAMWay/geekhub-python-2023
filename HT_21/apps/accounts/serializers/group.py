from django.contrib.auth.models import Group
from rest_framework import serializers


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api_accounts:group-detail")

    class Meta:
        model = Group
        fields = ['url', 'name']
