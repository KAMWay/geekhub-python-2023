from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.cart.models import Cart
from apps.products.models import Product


class CartSerializer(serializers.Serializer):
    items = serializers.ListSerializer(child=serializers.DictField())

    # session = serializers.CharField(max_length=255)

    class Meta:
        model = Cart
        fields = (
            'items',
            # 'session',
        )
        extra_kwargs = {
            'items': {'required': True},
        }

    def create(self, validated_data):
        return Cart(**validated_data)

    def validate_data(self, data):
        try:
            if data is None or not isinstance(data, dict):
                raise
            if data['product_id'] is None:
                raise
            quantity = int(data['quantity'])
            product = Product.objects.get(id=data['product_id'])
        except Exception:
            raise serializers.ValidationError(
                _(''),
                code='invalid_input_data'
            )

        return {'product_id': product.id, 'quantity': quantity}

    def update(self, instance: Cart, validated_data):
        product_id = validated_data['product_id']
        quantity = int(validated_data['quantity'])
        if quantity > 0:
            instance.update(product_id, quantity)
        else:
            instance.delete(product_id)
        return instance

    def is_valid(self, *, raise_exception=False):
        items = self.instance.items
        if items is None:
            return False
        for item in items:
            if not isinstance(item, dict):
                return False
            if not item.get('quantity', None) or not item.get('product_id', None):
                return False

        return True
