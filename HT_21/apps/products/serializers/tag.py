from rest_framework import serializers

from products.models import Tag


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)

    class Meta:
        model = Tag
        fields = [
            'id',
            'name'
        ]
