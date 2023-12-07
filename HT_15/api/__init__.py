import csv
import logging
import os

import requests

HTTP_TIMEOUT = 15
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'


class _Api:
    def _save_to_csv(self, data: list[dict], *, dirname, filename, delimiter: str = '|'):
        try:
            self.__save_file_csv(data, dirname=dirname, filename=filename, delimiter=delimiter)
            logging.info(f'successful save {filename}')
            print(f'successful save {filename}')
        except Exception:
            logging.error(f'invalid save {filename}')

    def __save_file_csv(self, data: list[dict], *, dirname, filename, delimiter: str = '|'):
        if dirname:
            self.__create_dir(dirname)
        file = os.path.join(dirname, filename) if dirname else filename

        fieldnames = [str(i) for i in data[0].keys()]
        with open(file, "w", newline='', encoding='UTF-8') as f:
            writer = csv.DictWriter(f, delimiter=delimiter, fieldnames=fieldnames)
            writer.writeheader()
            [writer.writerow(i) for i in data]

    def __create_dir(self, dirname):
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def _send_request(self, *, url: str, method: str = 'get', headers: dict = None, data=None) -> requests.Response:
        try:
            if headers is None:
                headers = {}

            headers.update({'User-Agent': USER_AGENT})
            response = self.__send(url=url, method=method, headers=headers, data=data)
            response.raise_for_status()
            return response
        except IOError:
            logging.error('invalid http request')
        finally:
            print(f'{method} {url}')
            logging.info(f'{method} {url}')

    def __send(self, *, url: str, method: str = 'get', headers=None, data=None) -> requests.Response:
        return requests.request(method=method, url=url, headers=headers, data=data, timeout=HTTP_TIMEOUT)
