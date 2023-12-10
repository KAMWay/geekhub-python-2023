# 2. Викорисовуючи requests, заходите на ось цей сайт "https://www.expireddomains.net/deleted-domains/"
# (з ним будьте обережні), вибираєте будь-яку на ваш вибір доменну зону і парсите список  доменів - їх там буде десятки
# тисяч (звичайно ураховуючи пагінацію). Всі отримані значення зберігти в CSV файл.
from dataclasses import dataclass
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from requests import Response

from api.base_api import BaseApi

BASE_URL = 'https://www.expireddomains.net/deleted-domains'
RESULTS_DIR = 'results'
RESULTS_FILENAME = 'domains.csv'


@dataclass
class Domain:
    name: str

    def dict(self) -> dict:
        return self.__dict__


class ExpiredDomainsApi(BaseApi):
    def __get_response(self, url: str) -> Response:
        sleep_time = 0 if url == BASE_URL else 5
        response = self._send_request(url=url, method='get', sleep_time=sleep_time)
        return response

    def __get_next_url(self, response_txt: str) -> [str, None]:
        soup = BeautifulSoup(response_txt, 'lxml')
        try:
            url = soup.select_one("a.next").get("href")
            return urljoin(BASE_URL, url)
        except AttributeError:
            return None

    def __parce_domains(self, response_txt: str) -> list[Domain]:
        soup = BeautifulSoup(response_txt, 'lxml')
        return [Domain(td.select_one('a').get_text()) for td in soup.select('td.field_domain')]

    def save_domains(self):
        self._remove_file(RESULTS_DIR, RESULTS_FILENAME)
        url = BASE_URL

        while url:
            response = self.__get_response(url)
            if not response:
                continue

            domains = self.__parce_domains(response.text)
            item_dict_list = [item.dict() for item in domains]
            self._save_to_csv(item_dict_list, filename=RESULTS_FILENAME, dirname=RESULTS_DIR, is_append=True)

            url = self.__get_next_url(response.text)


def start():
    api = ExpiredDomainsApi()
    api.save_domains()


if __name__ == '__main__':
    start()
