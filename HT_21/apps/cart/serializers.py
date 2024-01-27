from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.cart.models import Cart


class CartSerializer(serializers.Serializer):
    cart = serializers.CharField(read_only=True)

    class Meta:
        model = Cart
        fields = (
            'cart',
            # 'session',
        )
        extra_kwargs = {
            'cart': {'required': True},
        }

    def create(self, validated_data):
        return Cart(**validated_data)

    def validate_data(self, data):
        try:
            request_data = data.query_params
            if request_data is None or not isinstance(request_data, dict):
                raise
            if request_data['quantity'] is None:
                raise
            if not isinstance(int(request_data['product_id']), int):
                raise
        except Exception:
            raise serializers.ValidationError(
                _(''),
                code='invalid_input_data'
            )

        return {'product_id': request_data['product_id'], 'quantity': int(request_data['quantity'])}

    def update(self, instance: Cart, validated_data):
        product_id = validated_data['product_id']
        quantity = int(validated_data['quantity'])
        if quantity > 0:
            instance.update(product_id, quantity)
        else:
            instance.delete(product_id)
        return instance

    def is_valid(self, *, raise_exception=False):
        cart = self.instance.cart
        if cart is None:
            return False
        for item in cart:
            if not isinstance(item, dict):
                return False
            if not item.get('quantity', None) or not item.get('product_id', None):
                return False

        return True
