from rest_framework import serializers

from apps.products.models import Brand


class BrandSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(max_length=100)

    class Meta:
        fields = (
            'id',
            'name'
        )

    def create(self, validated_data):
        """
        Create and return a new `Brand` instance, given the validated data.
        """
        return Brand.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Brand` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.title)
        instance.save()
        return instance
