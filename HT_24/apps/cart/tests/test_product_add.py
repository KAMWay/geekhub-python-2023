from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from apps.products.tests.factories import UserFactory, ProductFactory


class CartAddTestCase(APITestCase):
    client: APIClient()
    maxDiff = None

    def setUp(self):
        self.client.force_authenticate(user=UserFactory())

    def test_add_exist_product_success(self):
        product = ProductFactory()
        response = self.client.post(
            path=reverse('api_cart:cart'),
            data={
                'quantity': 1,
                'product_id': product.id
            }
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code, msg=response.content)
        expected_data = {'items': [{'product_id': product.id, 'quantity': 1}, ]}
        self.assertDictEqual(expected_data, response.json(), msg=response.content)

        response = self.client.post(
            path=reverse('api_cart:cart'),
            data={
                'quantity': 1,
                'product_id': product.id
            }
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code, msg=response.content)
        expected_data = {'items': []}
        self.assertDictEqual(expected_data, response.json(), msg=response.content)

    def test_add_no_exist_product_failed(self):
        response = self.client.post(
            path=reverse('api_cart:cart'),
            data={
                'quantity': 1,
                'product_id': 'no_exist_product_id'
            }
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code, msg=response.content)

        response = self.client.post(
            path=reverse('api_cart:cart'),
            data={
                'quantity': 1,
                'product_id': 'no_exist_product_id'
            }
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code, msg=response.content)
        self.assertEqual(["Invalid input cart product data"], response.json(), msg=response.content)

    def test_add_exist_products_success(self):
        product1 = ProductFactory()
        product2 = ProductFactory()
        self.client.post(
            path=reverse('api_cart:cart'),
            data={
                'quantity': 1,
                'product_id': product1.id
            }
        )
        response = self.client.post(
            path=reverse('api_cart:cart'),
            data={
                'quantity': 2,
                'product_id': product2.id
            }
        )
        expected_data = {
            'items': [
                {'product_id': product1.id, 'quantity': 1},
                {'product_id': product2.id, 'quantity': 2},
            ]
        }
        self.assertDictEqual(expected_data, response.json(), msg=response.content)

        response = self.client.post(
            path=reverse('api_cart:cart'),
            data={
                'quantity': 3,
                'product_id': product1.id
            }
        )
        expected_data = {
            'items': [
                {'product_id': product2.id, 'quantity': 2},
            ]
        }
        self.assertDictEqual(expected_data, response.json(), msg=response.content)
