from rest_framework import serializers

from apps.products.models import ScrapyTask


class ScrapyTaskSerializer(serializers.ModelSerializer):
    # ids_str = serializers.ListField()
    # ids_str = serializers.CharField()

    class Meta:
        model = ScrapyTask
        fields = [
            'id',
            'ids_str'
        ]
