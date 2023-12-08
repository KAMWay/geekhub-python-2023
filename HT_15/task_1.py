# 1. Викорисовуючи requests, написати скрипт, який буде приймати на вхід ID категорії із сайту https://www.sears.com
# і буде збирати всі товари із цієї категорії, збирати по ним всі можливі дані (бренд, категорія, модель, ціна, рейтинг
# тощо) і зберігати їх у CSV файл (наприклад, якщо категорія має ID 12345, то файл буде називатись 12345_products.csv)


# Таска 1 - замінюємо сайт на https://www.sears.com
#  Завдання таке ж саме - на вхід отримуєте ІД категорії ("нижнього" типу, тобто це така категорія, в
#  якій відображаються продукти. # Наприклад, https://www.sears.com/tools-tool-storage/b-1025184 - відповідно,
#  ІД категорії - це 1025184)

# Підказка - відкрийте якусь категорію і досліджуйте запроси, які робить браузер, коли ви по ній щось робите -
# наприклад, переходите на наступну сторінку.
# Підказка 2 - не забувайте використовувати хедери


import json
import os
from dataclasses import dataclass
from urllib.parse import urljoin

from HT_15.api import _Api

RESULTS_DIR = 'results'


@dataclass
class SearsItem:
    brand_name: str
    name: str
    partNum: str
    source: str

    additional_attributes_dict: dict

    swatchesInd: bool
    offer_id: str
    upc: str
    value_consumer_rating: str
    text_consumer_rating: str

    lowest_price: float
    lowest_price_2: float
    final_price: float
    regular_price: float
    price_dict: dict

    show_cashback_badge: bool
    cashback_badge_category: str
    category: str

    def dict(self):
        return self.__dict__


class SearsApi(_Api):
    BASE_URL = 'https://www.sears.com'
    BASE_CATEGORY_URL = 'https://www.sears.com/content/configs/header/header.json'
    BASE_ITEMS_URL = 'https://www.sears.com/api/sal/v3/products/search'

    headers = {
        'authority': 'www.sears.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6,zh-TW;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://www.sears.com/',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',

        'authorization': 'SEARS',
        'content-type': 'application/json',
    }

    def __category_params(self, cat_group_id: int, start_index: int, end_index: int) -> dict:
        return {
            "startIndex": start_index,
            "endIndex": end_index,
            "searchType": "category",
            "catalogId": 12605,
            "store": "Sears",
            "storeId": 10153,
            "zipCode": 10101,
            "bratRedirectInd": "true",
            "catPredictionInd": "true",
            "disableBundleInd": "true",
            "filterValueLimit": 500,
            "includeFiltersInd": "true",
            "shipOrDelivery": "true",
            "solrxcatRedirection": "true",
            "sortBy": "ORIGINAL_SORT_ORDER",
            "whiteListCacheLoad": "false",
            "eagerCacheLoad": "true",
            "slimResponseInd": "true",
            "catGroupId": cat_group_id
            # 'seoURLPath': "food-grocery-snacks-nuts-seeds-trail-mixes/1038536"
        }

    def get_items(self, category_id: int) -> list[SearsItem]:
        if not category_id:
            return []

        filename = f'{category_id}.csv'
        self.__remove_file(filename)

        items_list = []
        for items in self.__get_items_json(category_id):
            self.__save_to_csv(filename, items)
            items_list += items

        return items_list

    def __remove_file(self, filename):
        file = os.path.join(RESULTS_DIR, filename)
        if os.path.isfile(file):
            os.remove(file)

    def __save_to_csv(self, filename: str, items: list[SearsItem]):
        item_dict_list = [item.dict() for item in items]
        self._save_to_csv(item_dict_list, filename=filename, dirname=RESULTS_DIR, is_append=True)

    def __get_items_json(self, category_id: int):
        start_index, end_index = 1, 48
        while True:
            print(f"start parsed items [{start_index}-{end_index}]:")

            params = self.__category_params(category_id, start_index, end_index)
            response = self._send_request(url=self.BASE_ITEMS_URL, method='get', headers=self.headers, params=params,
                                          sleep_time=20)
            if not response:
                break

            yield [self.__parse_sears_item(item) for item in json.loads(response.text)['items']]

            start_index += 48
            end_index += 48

    def __parse_sears_item(self, item_dict: dict) -> SearsItem:
        return SearsItem(
            brand_name=item_dict.get("brandName"),
            name=item_dict.get("name"),
            partNum=item_dict.get("partNum"),
            source=item_dict.get("source"),

            additional_attributes_dict=item_dict.get("additionalAttributes"),
            swatchesInd=self.__get_bool_value(item_dict.get("swatchesInd")),
            offer_id=item_dict.get("offerId"),
            upc=item_dict.get("upc"),
            value_consumer_rating=item_dict.get("valueConsumerRating"),
            text_consumer_rating=self.__get_none_value(item_dict.get("textConsumerRating")),

            lowest_price=self.__get_float_value(item_dict.get("lowest_price")),
            lowest_price_2=self.__get_float_value(item_dict.get("lowestPrice")),
            final_price=self.__get_float_value(item_dict.get("price").get("finalPrice")),
            regular_price=self.__get_float_value(item_dict.get("price").get("regularPrice")),
            price_dict=item_dict.get("price"),

            show_cashback_badge=item_dict.get("showCashbackBadge"),
            cashback_badge_category=item_dict.get("cashbackBadgeCategory"),
            category=item_dict.get("category")
        )

    def __get_categories_json(self):
        try:
            response = self._send_request(url=self.BASE_CATEGORY_URL, method='get', headers=self.headers, sleep_time=10)
            jsons_list = response.json()
            return next(i for i in jsons_list if i['itemId'] == 'shop')
        except Exception:
            return

    def get_category_url_by_json(self, category_id: str, item_dict: dict = None) -> [str, None]:
        if not item_dict:
            item_dict = self.__get_categories_json()
            if not item_dict:
                return

        path_item = item_dict.get('path')
        if path_item and f'b-{category_id}' in path_item:
            return urljoin(self.BASE_URL, path_item)

        children_items = item_dict.get('children')
        if not children_items:
            return

        for item_dict in children_items:
            rez = self.get_category_url_by_json(category_id, item_dict)
            if rez:
                return rez

    def get_category_url(self, category_id: int) -> [str, None]:
        if not category_id:
            return

        items_str = self.__get_categories_json()
        if not items_str:
            return
        else:
            items_str = str(items_str)

        index = items_str.index(f'b-{category_id}')
        if not index:
            return

        start_url = items_str.rfind('path', 0, index)
        end_url = items_str.find('}', index)

        if start_url and end_url:
            url = items_str[start_url + 9:end_url - 1]
            return urljoin(self.BASE_URL, url)

    def __get_float_value(self, value: str):
        try:
            return float(value)
        except TypeError:
            return

    def __get_none_value(self, value: str):
        try:
            return None if value == 'null' else value
        except TypeError:
            return None

    def __get_bool_value(self, value: str):
        try:
            return value and value == 'true'
        except TypeError:
            return False


def get_id_from_console() -> int:
    try:
        number = int(input('Enter category id number: '))
        if 0 <= number:
            return number
        raise ValueError()
    except ValueError:
        print('Incorrect input.')


def start():
    app = SearsApi()
    category_id = get_id_from_console()

    # category_id = '1025184'
    url = app.get_category_url(category_id)
    if url:
        print(f'Category {category_id} exist')
        app.get_items(category_id)
        print('Done')
    else:
        print('Category not found')


if __name__ == '__main__':
    start()
