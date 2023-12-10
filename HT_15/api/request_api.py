import logging
from random import randrange
from time import sleep

import requests

HTTP_TIMEOUT = 15
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'


class RequestApi:

    def _send_request(self, *, url: str, method: str = 'get', sleep_time: int, headers: dict = None,
                      params=None) -> requests.Response:
        try:
            if not headers:
                headers = {}

            headers.update({'User-Agent': USER_AGENT})
            sleep(randrange(sleep_time, sleep_time + 5, 1))
            response = requests.request(method=method, url=url, headers=headers, params=params, timeout=HTTP_TIMEOUT)
            response.raise_for_status()

            return response
        except IOError:
            logging.error('invalid http request')
        finally:
            print(f'{method} {url}')
            logging.info(f'{method} {url}')
