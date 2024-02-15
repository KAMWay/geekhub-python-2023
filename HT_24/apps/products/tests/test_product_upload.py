from unittest.mock import patch

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from apps.products.tests.factories import UserFactory, ProductFactory


class ProductUploadTestCase(APITestCase):
    client: APIClient()
    maxDiff = None

    @patch('apps.tasks.scraping_items.apply_async')
    def test_api_upload_product_success(self, mocked_task):
        self.client.force_authenticate(user=UserFactory(is_superuser=True, is_staff=True))

        product = ProductFactory()
        response = self.client.post(
            path=reverse('api_products:products-list'),
            data={
                'ids': f'{product.id}',
            }
        )

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code, msg=response.content)
        mocked_task.assert_called_once_with(ids=[product.id, ])
