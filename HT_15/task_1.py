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

import csv
import requests

from bs4 import BeautifulSoup
from random import randrange
from time import sleep

from requests import Request, Response, Session

BASE_URL = "https://www.sears.com/fitness-sports-fitness-exercise-strength-weight-training-home-gyms-stations/b-1340931236"
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'

class Product:
    def __init__(self, img_url: str, price: float, final_price: float, info: str, buy_url: str,
                 seller_info: str, is_flash_sale: bool = False):
        self.img_url = img_url
        self.price = price
        self.final_price = final_price
        self.info = info
        self.buy_url = buy_url
        self.seller_info = seller_info
        self.is_flash_sale = is_flash_sale


def map_product(response_text: str) -> Product:
    soup = BeautifulSoup(response_text, 'lxml')
    return Product(
        img_url=soup.select_one("a").get("href"),
        price=float(soup.select_one("del").select_one("span.money").get_text()),
        final_price=float(soup.select_one("span.final-price-display").get_text()),
        info=soup.select_one("div.custom-div-title").get_text(),
        buy_url=soup.select_one("div.product-detail sale-new-block").select_one("a").get("href"),
        seller_info=soup.select_one("div.seller-info ").get_text(),
        is_flash_sale=True if soup.select_one("div.best-promo").get_text() else False
    )


def map_products(response: requests.Response):
    soup = BeautifulSoup(response.text, 'lxml')
    for i in soup.select('div.product-box'):
        yield map_product(i)


def write_csv(data: list[dict], path: str = 'quote.csv', delimiter: str = '|'):
    if not data or not data[0]:
        return

    field_names = [str(i) for i in data[0].keys()]
    with open(path, "w", newline='', encoding='UTF-8') as f:
        writer = csv.DictWriter(f, delimiter=delimiter, fieldnames=field_names)
        writer.writeheader()
        [writer.writerow(i) for i in data]


def get_response(url, *, method: str = 'get'):
    try:
        yield Request(
            url=url,
            method=method,
            callback=ddd,
        )

        # response = requests.request(method=method, url=url)
        # sleep(randrange(1, 3, 1))
        # response.raise_for_status()
        # return response
    finally:
        print(f"{method} {url}")


def ddd(response:Response):
    soup = BeautifulSoup(response.text, 'lxml')
    if soup.select_one('div.loading-more'):
        yield response


def is_end(response_text: str) -> bool:
    soup = BeautifulSoup(response_text, 'lxml')
    a = soup.select_one('div.loading-more')
    return a is not None


def start():
    url = BASE_URL

    s = Session()

    req = Request('get', url, headers={'User-Agent':USER_AGENT})
    prepped = req.prepare()

    # do something with prepped.body
    prepped.body = 'No, I want exactly this as the body.'

    # do something with prepped.headers
    # del prepped.headers['Content-Type']
    resp = s.send(prepped,
                  timeout=15
                  )

    print(resp.status_code)

    #
    # resp = s.send(prepped,
    #               stream=stream,
    #               verify=verify,
    #               proxies=proxies,
    #               cert=cert,
    #               timeout=timeout
    #               )

    response = get_response(url)
    while not is_end(response.text):
        response = get_response(url, method='post')

    aaa = [map_products(response)]
    requests.get(timeout=15, headers={'User-Agent':USER_AGENT, 'Authorization':'SEARS'}, url='https://www.sears.com/api/sal/v3/products/search?startIndex=1&endIndex=48&searchType=category&catalogId=12605&store=Sears&storeId=10153&zipCode=10101&bratRedirectInd=true&catPredictionInd=true&disableBundleInd=true&filterValueLimit=500&includeFiltersInd=true&shipOrDelivery=true&solrxcatRedirection=true&sortBy=ORIGINAL_SORT_ORDER&whiteListCacheLoad=false&eagerCacheLoad=true&slimResponseInd=true&catGroupId=1031416&seoURLPath=appliances-refrigerators-french-door-refrigerators/1031416')
    requests.get(timeout=15, headers={'User-Agent': USER_AGENT, 'Authorization': 'SEARS'},
                 url='https://www.sears.com/api/sal/v3/products/search?startIndex=1&endIndex=48&searchType=category&catalogId=12605&store=Sears&storeId=10153&zipCode=10101&bratRedirectInd=true&catPredictionInd=true&disableBundleInd=true&filterValueLimit=500&includeFiltersInd=true&shipOrDelivery=true&solrxcatRedirection=true&sortBy=ORIGINAL_SORT_ORDER&whiteListCacheLoad=false&eagerCacheLoad=true&slimResponseInd=true&catGroupId=1031416&seoURLPath=appliances-refrigerators-french-door-refrigerators/1031416')
    requests.get(timeout=15, headers={'User-Agent': USER_AGENT, 'Authorization': 'SEARS'},
                 url='https://www.sears.com/api/sal/v3/products/search?whiteListCacheLoad=false&storeId=10153&catGroupId=1025184')
    #     soup = BeautifulSoup(response.text, 'lxml')
    #     is_end(response)
    #     soup.select_one("li.next")
    #
    #     response = get_response()
    #
    #
    #     soup = BeautifulSoup(response.text, 'lxml')
    #     [quotes.append(map_quote(quote_soup)) for quote_soup in soup.select("div.quote")]
    #
    #     url = soup.select_one("li.next")
    #     if url:
    #         url = URL + url.select_one("a").get("href")
    #
    # dict_quotes = [{'text': i.text, 'author': i.author, 'author_link': i.author_link, 'tags': i.tags} for i in quotes]
    # write_csv(dict_quotes)


if __name__ == '__main__':
    start()
