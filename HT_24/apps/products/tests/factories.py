import factory
from django.contrib.auth.models import User

from apps.products.models import Product, Brand, Category


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')
    password = factory.PostGenerationMethodCall('set_password', 'password')


    class Meta:
        model = User


class BrandFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda i: f'BrandName{i}')

    class Meta:
        model = Brand


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda i: f'CategoryName{i}')

    class Meta:
        model = Category


class ProductFactory(factory.django.DjangoModelFactory):
    regular_price = 10
    sale_price = 5
    store_id = 1

    name = factory.Faker('name')
    id = factory.Sequence(lambda i: f'product{i}')
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = Product
