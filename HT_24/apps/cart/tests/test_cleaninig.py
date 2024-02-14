from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from apps.products.tests.factories import UserFactory, ProductFactory


class AddItemTestCase(APITestCase):
    client: APIClient()
    maxDiff = None

    def setUp(self):
        self.client.force_authenticate(user=UserFactory())

    def test_cleaning_cart_success(self):
        response = self.client.delete(
            path=reverse('api_cart:cart'),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=response.content)

        self.client.put(
            path=reverse('api_cart:cart'),
            data={
                'quantity': 1,
                'product_id': ProductFactory().id
            }
        )
        self.client.put(
            path=reverse('api_cart:cart'),
            data={
                'quantity': 2,
                'product_id': ProductFactory().id
            }
        )
        self.client.put(
            path=reverse('api_cart:cart'),
            data={
                'quantity': 3,
                'product_id': ProductFactory().id
            }
        )
        response = self.client.delete(
            path=reverse('api_cart:cart'),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=response.content)
