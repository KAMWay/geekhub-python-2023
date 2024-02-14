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

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code, msg=response.content)
        response = self.client.get(
            path=reverse('api_cart:cart'),
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code, msg=response.content)
        expected_data = {'items': []}
        self.assertDictEqual(expected_data, response.json(), msg=response.content)
