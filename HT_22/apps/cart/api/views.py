from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.api.tags import CART_TAG
from apps.cart.models import Cart
from apps.cart.serializers import CartSerializer


@extend_schema(
    tags=[CART_TAG],
)
class CartApiView(APIView):

    @extend_schema(
        examples=[
            OpenApiExample(
                'Example Value',
                value={
                    "items": "[{'product_id': 'string', 'quantity': 1}]"
                },
            ),
        ],
        responses=CartSerializer,
    )
    def get(self, request):
        cart = Cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @extend_schema(
        examples=[
            OpenApiExample(
                'Example Value',
                value={
                    'product_id': 'string',
                    'quantity': 1
                },
            ),
        ],
        request=CartSerializer,
    )
    def post(self, request):
        cart = Cart(request)

        serializer = CartSerializer(cart)
        validate_data = serializer.validate_data(request.data)
        if cart.select_product(validate_data['product_id']) is not None:
            validate_data['quantity'] = 0

        serializer.update(cart, validate_data)

        return Response(serializer.data)

    @extend_schema(
        examples=[
            OpenApiExample(
                'Example Value',
                value={
                    'product_id': 'string',
                    'quantity': 1
                },
            ),
        ],
        request=CartSerializer,
    )
    def put(self, request):
        cart = Cart(request)
        serializer = CartSerializer(cart)
        validate_data = serializer.validate_data(request.data)
        serializer.update(cart, validate_data)

        return Response(serializer.data)

    def delete(self, request):
        cart = Cart(request)
        cart.clear()

        return Response(status=status.HTTP_204_NO_CONTENT)
