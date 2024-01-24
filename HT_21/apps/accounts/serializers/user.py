from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="accounts:user-detail")

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']
