from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
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
        request=CartSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                description='Product by ID has been added to the cart',
                response=CartSerializer,
            ),
            status.HTTP_200_OK: OpenApiResponse(
                description='Product by id was be exist and removed from cart',
                response=CartSerializer,
            ),
        },
    )
    def post(self, request):
        cart = Cart(request)

        serializer = CartSerializer(cart)
        validate_data = serializer.validate_data(request.data)

        is_exist = cart.select_product(validate_data['product_id']) is not None
        if is_exist:
            validate_data['quantity'] = 0

        serializer.update(cart, validate_data)

        if is_exist:
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @extend_schema(
        request=CartSerializer,
        responses=CartSerializer,
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
