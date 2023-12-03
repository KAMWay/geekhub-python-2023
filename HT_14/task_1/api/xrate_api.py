from datetime import datetime

import requests

from HT_14.task_1.model import XRate, ATMException

HTTP_TIMEOUT = 15


class _XRateApi:
    def _update_rate(self, xrate: XRate):
        xrate.updated = datetime.now()

    def _get_request(self, *, url: str, params=None, data=None, headers=None):
        try:
            response = requests.get(url=url, data=data, params=params, headers=headers, timeout=HTTP_TIMEOUT)
            response.raise_for_status()
            return response
        except Exception:
            raise ATMException("invalid http request")


class PrivatApi(_XRateApi):
    def __get_response_json(self) -> list[dict]:
        response = self._get_request(url="https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
        # dt = datetime.strptime(response.headers['date'], '%a, %d %b %Y %H:%M:%S %Z')
        return response.json()

    def _get_rate(self, from_currency: str) -> XRate:
        rate_aliases = {"USD", "EUR"}

        if from_currency.upper() not in rate_aliases:
            raise ATMException(f"invalid from currency: {from_currency}")

        try:
            return next((self.__map_xrate(json_data) for json_data in self.__get_response_json()
                         if json_data['ccy'] == from_currency), None)
        except (KeyError, ValueError):
            raise ATMException("invalid json rate data")

    def _get_rates(self) -> list[XRate]:
        try:
            return [self.__map_xrate(json_data) for json_data in self.__get_response_json()]
        except (KeyError, ValueError):
            raise ATMException("invalid json rates data")

    @staticmethod
    def __map_xrate(json_data: dict) -> XRate:
        base_currency = json_data['base_ccy'].upper()
        to_currency = json_data['ccy'].upper()
        buy_rate = float(json_data['buy'])
        sale_rate = float(json_data['sale'])
        return XRate(base_currency, to_currency, buy_rate, sale_rate)
