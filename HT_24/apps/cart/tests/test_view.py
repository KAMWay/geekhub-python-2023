from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from apps.products.tests.factories import UserFactory, ProductFactory


class AddItemTestCase(APITestCase):
    client: APIClient()
    maxDiff = None

    def test_view_authenticated_user_success(self):
        self.client.force_authenticate(user=UserFactory())

        response = self.client.get(
            path=reverse('api_cart:cart'),
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code, msg=response.content)
        expected_data = {'items': []}
        self.assertDictEqual(expected_data, response.json(), msg=response.content)

        product1 = ProductFactory()
        product2 = ProductFactory()
        product3 = ProductFactory()
        self.client.post(
            path=reverse('api_cart:cart'),
            data={
                'quantity': 1,
                'product_id': product1.id
            }
        )
        self.client.post(
            path=reverse('api_cart:cart'),
            data={
                'quantity': 1,
                'product_id': product2.id
            }
        )
        self.client.post(
            path=reverse('api_cart:cart'),
            data={
                'quantity': 1,
                'product_id': product3.id
            }
        )
        response = self.client.get(
            path=reverse('api_cart:cart'),
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code, msg=response.content)
        expected_data = {
            'items': [
                {'product_id': product1.id, 'quantity': 1},
                {'product_id': product2.id, 'quantity': 1},
                {'product_id': product3.id, 'quantity': 1},
            ]
        }
        self.assertDictEqual(expected_data, response.json(), msg=response.content)

    def test_view_not_authenticated_user_failed(self):
        response = self.client.get(
            path=reverse('api_cart:cart'),
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code, msg=response.content)
        self.assertDictEqual(
            response.json(),
            {"detail": "Authentication credentials were not provided."},
            msg=response.content
        )
