import json
import logging
from random import randint
from time import sleep
from urllib.parse import urljoin

import requests

from apps.products.models import Product
from apps.products.models import Brand

logger = logging.getLogger('django')


class ScrapingTask:
    DETAIL_URL = 'https://www.sears.com/api/sal/v3/products/details/'

    HEADERS = {
        'authority': 'www.sears.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6,zh-TW;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'authorization': 'SEARS',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    PARAMS = {
        'storeName': 'Sears',
        'memberStatus': 'G',
        'zipCode': '10101',
    }

    def __init__(self, ids: set):
        self.__ids = ids

    def run(self):
        logger.info('Task scrapping items start')
        for _id in self.__ids:
            product = self.__scrap_by_id(_id)
            if product:
                try:
                    product.save()
                    logger.info(f'Product by id {_id} save successful')
                except Exception as e:
                    logger.error(f'Product by id {_id} save unsuccessful: {e}')
        logger.info('Task scrapping items done')

    def __scrap_by_id(self, product_id: str) -> Product:
        logger.info(f'Start scrapping product by id: {product_id}')
        try:
            sleep(randint(20, 30))
            response = requests.get(urljoin(self.DETAIL_URL, product_id), params=self.PARAMS, headers=self.HEADERS, )
            response.raise_for_status()
            product_dict = json.loads(response.text)['productDetail']['softhardProductdetails'][0]
            return self.__parse_product(product_dict)
        except Exception as e:
            logger.error(f"Can't scraping product by id: {product_id}: {e}")
        finally:
            logger.info(f'Stop scrapping product by id: {product_id}')

    def __parse_product(self, product_dict: dict) -> Product:
        url = product_dict.get('seoUrl')

        default_seller = product_dict.get('defaultSeller')
        if default_seller:
            default_seller = default_seller.get('sellerId')

        brand = self.__get_brand_by_name(self.__to_str_value(product_dict.get('brandName')))

        return Product(
            id=self.__parse_id(url),

            brand=brand,
            name=self.__to_str_value(product_dict.get('descriptionName')),
            main_image_url=self.__to_str_value(product_dict.get('mainImageUrl')),
            description=self.__to_str_value(product_dict.get('shortDescription')),
            url=self.__to_str_value(url),

            regular_price=self.__to_float_value(product_dict.get('regularPrice')),
            sale_price=self.__to_float_value(product_dict.get('salePrice')),

            default_seller_id=self.__to_str_value(default_seller),
            store_id=self.__to_int_value(product_dict.get('storeId')),
        )

    def __get_brand_by_name(self, name: str) -> Brand:
        brand = Brand.objects.filter(name=name).first()
        if brand:
            return brand

        return Brand.objects.create(name=name)

    def __parse_id(self, url: str) -> str:
        start_id = url.rfind('p-')
        start_id = (start_id + 2) if start_id >= 0 else 0

        end_id = url.find('?', start_id)
        end_id = len(url) if end_id < 0 else end_id

        return url[start_id:end_id]

    def __to_float_value(self, value: str) -> float:
        try:
            return float(value)
        except TypeError:
            return 0

    def __to_int_value(self, value: str) -> int:
        try:
            return int(value)
        except TypeError:
            return 0

    def __to_str_value(self, value: str) -> str:
        return str(value) if value else ""
