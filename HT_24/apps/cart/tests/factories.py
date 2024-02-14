import factory
from django.contrib.auth.models import User

from apps.cart.models import Cart
from apps.products.models import Product, Brand

TEST_PASSWORD = 'password'


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')
    password = factory.PostGenerationMethodCall('set_password', TEST_PASSWORD)

    class Meta:
        model = User


class BrandFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda i: f'BrandName{i}')

    class Meta:
        model = Brand


class ProductFactory(factory.django.DjangoModelFactory):
    regular_price = 10
    sale_price = 5
    store_id = 1
    brand = factory.SubFactory(BrandFactory)
    name = factory.Faker('name')
    id = factory.Sequence(lambda i: f'product{i}')

    class Meta:
        model = Product


class CartFactory(factory.django.DjangoModelFactory):
    request = "example_request"

    # session = factory.Faker('sha256')
    # items = []

    class Meta:
        model = Cart
