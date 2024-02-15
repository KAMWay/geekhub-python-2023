from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from apps.products.tests.factories import ProductFactory, CategoryFactory, BrandFactory, UserFactory


class ProductAccessTestCase(APITestCase):
    client: APIClient()
    maxDiff = None

    def test_api_products_access_failed(self):
        product = ProductFactory()
        self.check_default_methods_case(reverse('api_products:products-list'), product.id)
        self.client.force_authenticate(user=UserFactory())
        self.check_default_methods_case(reverse('api_products:products-list'), product.id)

    def test_api_categories_access_failed(self):
        category = CategoryFactory()
        self.check_default_methods_case(reverse('api_products:categories-list'), category.id)
        self.client.force_authenticate(user=UserFactory())
        self.check_default_methods_case(reverse('api_products:categories-list'), category.id)

    def test_api_brands_access_failed(self):
        brand = BrandFactory()
        self.check_default_methods_case(reverse('api_products:brands-list'), brand.id)
        self.client.force_authenticate(user=UserFactory())
        self.check_default_methods_case(reverse('api_products:brands-list'), brand.id)

    def check_default_methods_case(self, url, _id):
        response = self.client.get(path=url, )
        self.assertEqual(status.HTTP_200_OK, response.status_code, msg=response.content)
        response = self.client.post(path=url, )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code, msg=response.content)

        response = self.client.get(path=f'{url}{_id}/', )
        self.assertEqual(status.HTTP_200_OK, response.status_code, msg=response.content)
        response = self.client.put(path=f'{url}{_id}/', )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code, msg=response.content)
        response = self.client.patch(path=f'{url}{_id}/', )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code, msg=response.content)
        response = self.client.delete(path=f'{url}{_id}/', )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code, msg=response.content)
