from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from apps.cart.tests.factories import UserFactory, ProductFactory


class AddItemTestCase(APITestCase):
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.content)
        self.assertDictEqual(
            response.json().get('items')[0],
            {'product_id': product.id, 'quantity': 1},
            msg=response.content
        )

        response = self.client.post(
            path=reverse('api_cart:cart'),
            data={
                'quantity': 1,
                'product_id': product.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.content)
        self.assertEqual(
            response.json().get('items'),
            [],
            msg=response.content
        )

    def test_add_no_exist_product_failed(self):
        response = self.client.post(
            path=reverse('api_cart:cart'),
            data={
                'quantity': 1,
                'product_id': 'no_exist_product_id'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.content)

        response = self.client.post(
            path=reverse('api_cart:cart'),
            data={
                'quantity': 1,
                'product_id': 'no_exist_product_id'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.content)
        self.assertEqual(
            response.json(),
            ["Invalid input cart product data"],
            msg=response.content
        )

    def test_update_exist_product_success(self):
        product = ProductFactory()
        response = self.client.put(
            path=reverse('api_cart:cart'),
            data={
                'quantity': 1,
                'product_id': product.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.content)
        self.assertDictEqual(
            response.json().get('items')[0],
            {'product_id': product.id, 'quantity': 1},
            msg=response.content
        )

        response = self.client.put(
            path=reverse('api_cart:cart'),
            data={
                'quantity': 2,
                'product_id': product.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.content)
        self.assertDictEqual(
            response.json().get('items')[0],
            {'product_id': product.id, 'quantity': 2},
            msg=response.content
        )

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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.content)
        self.assertTrue(
            len(response.json().get('items')) == 2,
            msg=response.content
        )
        self.assertTrue(
            {'product_id': product1.id, 'quantity': 1} in response.json().get('items'),
            msg=response.content
        )
        self.assertTrue(
            {'product_id': product2.id, 'quantity': 2} in response.json().get('items'),
            msg=response.content
        )

        response = self.client.post(
            path=reverse('api_cart:cart'),
            data={
                'quantity': 3,
                'product_id': product1.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.content)
        self.assertTrue(
            len(response.json().get('items')) == 1,
            msg=response.content
        )
        self.assertTrue(
            {'product_id': product2.id, 'quantity': 2} in response.json().get('items'),
            msg=response.content
        )

    def test_update_exist_products_success(self):
        product1 = ProductFactory()
        self.client.put(
            path=reverse('api_cart:cart'),
            data={
                'quantity': 1,
                'product_id': product1.id
            }
        )
        self.client.put(
            path=reverse('api_cart:cart'),
            data={
                'quantity': 2,
                'product_id': ProductFactory().id
            }
        )
        response = self.client.put(
            path=reverse('api_cart:cart'),
            data={
                'quantity': 3,
                'product_id': product1.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.content)
        self.assertTrue(
            len(response.json().get('items')) == 2,
            msg=response.content
        )
        self.assertTrue(
            {'product_id': product1.id, 'quantity': 3} in response.json().get('items'),
            msg=response.content
        )

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
