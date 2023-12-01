# 3. http://quotes.toscrape.com/ - написати скрейпер для збору всієї доступної інформації про записи: цитата,
# автор, інфа про автора тощо.
#     - збирається інформація з 10 сторінок сайту.
#     - зберігати зібрані дані у CSV файл
import csv

import requests

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
    text = quote_soup.select_one("span.text").get_text()[1:-1]
    author = quote_soup.select_one("small.author").get_text()
    author_link = URL + quote_soup.select_one("a").get("href")
    tags = [{tag.get_text(): URL + tag.get("href")} for tag in quote_soup.select("a.tag")]

    return Quote(text, author, author_link, tags)


def write_csv(data: list[dict], path: str = 'quote.csv', delimiter: str = '|'):
    if not data or not data[0]:
        return

    field_names = [str(i) for i in data[0].keys()]
    with open(path, "w", newline='', encoding='UTF-8') as f:
        writer = csv.DictWriter(f, delimiter=delimiter, fieldnames=field_names)
        writer.writeheader()
        [writer.writerow(i) for i in data]


def start():
    url = URL
    quotes = []
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        [quotes.append(map_quote(quote_soup)) for quote_soup in soup.select("div.quote")]

        url = soup.select_one("li.next")
        if url:
            url = URL + url.select_one("a").get("href")

    dict_quotes = [{'text': i.text, 'author': i.author, 'author_link': i.author_link, 'tags': i.tags} for i in quotes]
    write_csv(dict_quotes)


if __name__ == '__main__':
    start()
