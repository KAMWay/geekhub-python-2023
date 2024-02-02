from rest_framework import serializers

from apps.products.models import Product
from .category import CategorySerializer
from .tag import TagSerializer


class ProductSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source="brand.name", read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'main_image_url',
            'description',
            'url',
            'regular_price',
            'sale_price',
            'default_seller_id',
            'store_id',
            'tags',
            'category',
            'brand',
            'brand_name',
        ]
