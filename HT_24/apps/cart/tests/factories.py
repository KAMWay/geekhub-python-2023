import factory

from apps.cart.models import Cart


class CartFactory(factory.django.DjangoModelFactory):
    request = "example_request"

    class Meta:
        model = Cart
