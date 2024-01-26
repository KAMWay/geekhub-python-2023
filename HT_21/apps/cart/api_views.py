from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.api_tags import CART_TAG
from cart.models import Cart
from cart.serializers import CartSerializer


@extend_schema(
    tags=[CART_TAG],
)
class CartApiView(APIView):

    @extend_schema(
        examples=[
            OpenApiExample(
                'Example Value',
                value={
                    "cart": "[{'product_id': 'string', 'quantity': 1}]"
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
        validate_data = serializer.validate_data(request)
        if cart.select_product(validate_data['product_id']) is not None:
            validate_data['quantity'] = 0

        serializer.update(cart, validate_data)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        tags=[CART_TAG],
        examples=[
            OpenApiExample(
                'Example Value',
                # summary='short summary',
                # description='longer description',
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

        validate_data = serializer.validate_data(request)
        serializer.update(cart, validate_data)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request):
        cart = Cart(request)
        cart.clear()

        return Response(status=status.HTTP_204_NO_CONTENT)
