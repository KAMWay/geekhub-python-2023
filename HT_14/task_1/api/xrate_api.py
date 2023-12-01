from datetime import datetime

import requests

from HT_14.task_1.model import XRate, ATMException

HTTP_TIMEOUT = 15


class _XRateApi:
    def _update_rate(self, xrate: XRate):
        xrate.updated = datetime.now()

    def _get_request(self, *, url: str, data=None, headers=None):
        try:
            response = requests.get(url=url, data=data, headers=headers, timeout=HTTP_TIMEOUT)
            return response
        except Exception as ex:
            raise ATMException("can't do http request")


class PrivatApi(_XRateApi):
    def _get_response_json(self) -> dict:
        response = self._get_request(url="https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
        # dt = datetime.strptime(response.headers['date'], '%a, %d %b %Y %H:%M:%S %Z')
        return response.json()

    def _get_rate(self, response_json: list[dict], from_currency: str) -> XRate:
        rate_aliases = {"USD", "EUR"}

        if from_currency.upper() not in rate_aliases:
            raise ValueError(f"Invalid from_currency: {from_currency}")

        return next(
            (self.__map_xrate(json_data) for json_data in response_json if json_data['ccy'] == from_currency),
            None)

    def _get_rates(self, response_json: list[dict]) -> list[XRate]:
        return [self.__map_xrate(json_data) for json_data in response_json]

    @staticmethod
    def __map_xrate(json_data: dict) -> XRate:
        base_currency = json_data['base_ccy'].upper()
        to_currency = json_data['ccy'].upper()
        buy_rate = float(json_data['buy'])
        sale_rate = float(json_data['sale'])
        return XRate(base_currency, to_currency, buy_rate, sale_rate)


if __name__ == '__main__':
    pb = PrivatApi()
    data = pb._get_response_json()
    print(pb._get_rate(data, "USD"))
    print(pb._get_rates(data))
