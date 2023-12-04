# 3. http://quotes.toscrape.com/ - написати скрейпер для збору всієї доступної інформації про записи: цитата,
# автор, інфа про автора тощо.
#     - збирається інформація з 10 сторінок сайту.
#     - зберігати зібрані дані у CSV файл
import csv
import requests

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from bs4 import BeautifulSoup

URL = "http://quotes.toscrape.com"


class Quote:
    def __init__(self, text: str, author: str, author_link: str, tags: [list, None]):
        if tags is None:
            tags = []

        self.__text = text
        self.__author = author
        self.__author_link = author_link
        self.__tags = tags

    @property
    def text(self) -> str:
        return self.__text

    @property
    def author(self) -> str:
        return self.__author

    @property
    def author_link(self) -> str:
        return self.__author_link

    @property
    def tags(self) -> list:
        return self.__tags


def map_quote(quote_soup) -> Quote:
    try:
        text = quote_soup.select_one("span.text").get_text()[1:-1]
        author = quote_soup.select_one("small.author").get_text()
        author_link = URL + quote_soup.select_one("a").get("href")
        tags = [{tag.get_text(): URL + tag.get("href")} for tag in quote_soup.select("a.tag")]

        return Quote(text, author, author_link, tags)
    except Exception as e:
        print(f"{e}")


def write_csv(data: list[dict], path: str = 'quote.csv', delimiter: str = '|'):
    if not data or not data[0]:
        return

    field_names = [str(i) for i in data[0].keys()]
    with open(path, "w", newline='', encoding='UTF-8') as f:
        writer = csv.DictWriter(f, delimiter=delimiter, fieldnames=field_names)
        writer.writeheader()
        [writer.writerow(i) for i in data]


def get_response(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except IOError:
        print(f"invalid http request {url}")
    finally:
        print(f"Get {url}")


def thread_function(soup_dict: dict):
    try:
        print(f"Start parse in thread {soup_dict.get('url')}")
        return (map_quote(quote_soup) for quote_soup in soup_dict.get("soup").select("div.quote"))
    except Exception as e:
        print(f"Exception {e}")
    finally:
        print(f"Stop parse in thread {soup_dict.get('url')}")


def get_soups() -> list[dict]:
    url = URL
    while url:
        soup_dict = {}
        response = get_response(url)
        soup = BeautifulSoup(response.text, 'lxml')
        soup_dict['url'] = url
        soup_dict['soup'] = soup
        yield soup_dict

        url = soup.select_one("li.next")
        if url:
            url = URL + url.select_one("a").get("href")


def thread_with_map():
    quotes = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        for soup in get_soups():
            for results in executor.map(thread_function, (soup,)):
                for quote in results:
                    quotes.append(quote)
    return quotes


def thread_with_submit():
    quotes = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        for future in ((executor.submit(thread_function, soup)) for soup in list(get_soups())):
            for quote in future.result():
                quotes.append(quote)
    return quotes


def start():
    start = datetime.now()

    quotes = thread_with_submit()
    dict_quotes = [{'text': i.text, 'author': i.author, 'author_link': i.author_link, 'tags': i.tags} for i in quotes]
    write_csv(dict_quotes)

    print((datetime.now() - start).seconds)


if __name__ == '__main__':
    start()
