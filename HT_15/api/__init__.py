import csv
import logging
import os
from random import randrange
from time import sleep

import requests

HTTP_TIMEOUT = 15
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'


class _Api:
    def _save_to_csv(self, data: list[dict], *, dirname, filename, delimiter: str = '|', is_append: bool = False):
        try:
            self.__save_file_csv(data, dirname=dirname, filename=filename, delimiter=delimiter, is_append=is_append)
            logging.info(f'successful save {filename}')
            print(f'successful {"appended" if is_append else "written"} {filename}')
        except Exception:
            logging.error(f'invalid {"appended" if is_append else "written"} {filename}')

    def __save_file_csv(self, data: list[dict], *, dirname, filename, delimiter, is_append):
        if dirname:
            self.__create_dir(dirname)
        file = os.path.join(dirname, filename) if dirname else filename

        fieldnames = [str(i) for i in data[0].keys()]
        with open(file, "a" if is_append else "w", newline='', encoding='UTF-8') as f:
            writer = csv.DictWriter(f, delimiter=delimiter, fieldnames=fieldnames)

            if not is_append:
                writer.writeheader()

            [writer.writerow(i) for i in data]

    def __create_dir(self, dirname):
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def _send_request(self, *, url: str, method: str = 'get', sleep_time: int, headers: dict = None,
                      params=None) -> requests.Response:
        try:
            if not headers:
                headers = {}
            headers.update({'User-Agent': USER_AGENT})
            sleep(randrange(sleep_time, sleep_time + 5, 1))
            response = self.__send(url=url, method=method, headers=headers, params=params)
            response.raise_for_status()
            return response
        except IOError:
            logging.error('invalid http request')
        finally:
            print(f'{method} {url}')
            logging.info(f'{method} {url}')

    def __send(self, *, url: str, method: str = 'get', headers=None, params=None) -> requests.Response:
        return requests.request(method=method, url=url, headers=headers, params=params, timeout=HTTP_TIMEOUT)