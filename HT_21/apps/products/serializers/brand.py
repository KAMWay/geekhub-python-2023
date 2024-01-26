from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.products.models import Brand


class BrandSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(max_length=100)

    class Meta:
        model = Brand
        fields = (
            'id',
            'name'
        )

    def validate_name(self, name):
        if Brand.objects.filter(name__iexact=name):
            raise serializers.ValidationError(
                _(f'Brands {name} already exist'),
                code='invalid_brand_name'
            )

        return name
