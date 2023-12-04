# 2. Створіть програму для отримання курсу валют за певний період.
#     - отримати від користувача дату (це може бути як один день так і інтервал - початкова і кінцева дати,
#     продумайте механізм реалізації) і назву валюти
#     - вивести курс по відношенню до гривні на момент вказаної дати (або за кожен день у вказаному інтервалі)
#     - не забудьте перевірку на валідність введених даних
import datetime
from datetime import date

import requests

HTTP_TIMEOUT = 15

PRIVATE_PERIOD_EXCHANGE_URL = "https://api.privatbank.ua/p24api/exchange_rates?json"


class CustomException(Exception):
    pass


class XRate:
    def __init__(self, base_currency: str, to_currency: str, purchase_rate: float, sale_rate: float,
                 exchange_date: date = None):
        exchange_date = date.today() if not exchange_date else exchange_date
        self.__base_currency = base_currency
        self.__to_currency = to_currency
        self.__purchase_rate = purchase_rate
        self.__sale_rate = sale_rate
        self.__exchange_date = exchange_date

    @property
    def base_currency(self) -> str:
        return self.__base_currency

    @base_currency.setter
    def base_currency(self, base_currency: str):
        self.__base_currency = base_currency

    @property
    def to_currency(self) -> str:
        return self.__to_currency

    @to_currency.setter
    def to_currency(self, to_currency: str):
        self.__to_currency = to_currency

    @property
    def purchase_rate(self) -> float:
        return self.__purchase_rate

    @purchase_rate.setter
    def purchase_rate(self, purchase_rate: float):
        self.__purchase_rate = purchase_rate

    @property
    def sale_rate(self) -> float:
        return self.__sale_rate

    @sale_rate.setter
    def sale_rate(self, sale_rate: float):
        self.__sale_rate = sale_rate

    @property
    def exchange_date(self) -> date:
        return self.__exchange_date

    @exchange_date.setter
    def exchange_date(self, exchange_date: float):
        self.__exchange_date = exchange_date


class _XRateApi:
    def _get_request(self, *, url: str, params=None):
        try:
            response = requests.get(url=url, params=params, timeout=HTTP_TIMEOUT)
            response.raise_for_status()
            return response
        except Exception:
            raise CustomException("invalid http request")


class PrivatApi(_XRateApi):
    def __get_response_json(self, *, params: [dict, None] = date.today()) -> dict:
        response = self._get_request(url=PRIVATE_PERIOD_EXCHANGE_URL, params=params)
        return response.json()

    def get_currency_rates(self, currency_name: str, dates: list):
        if currency_name not in self.rate_aliases():
            raise CustomException(f"invalid currency: {currency_name}")

        if not dates:
            raise CustomException(f"invalid dates")

        for dt in dates:
            try:
                yield next(i for i in self._get_rates(dt) if i.to_currency == currency_name)
            except (KeyError, TypeError):
                raise CustomException("invalid json data")
            except StopIteration:
                raise CustomException(f"invalid json parse currency: {currency_name}")

    def _get_rates(self, dt: date) -> list[XRate]:
        if not date:
            raise CustomException(f"invalid date")

        exchange_rates = self.__get_response_json(params={'date': str(dt.strftime("%d.%m.%Y"))})["exchangeRate"]
        return [self.__map_xrate(dt, json_data) for json_data in exchange_rates]

    @staticmethod
    def __map_xrate(exchange_date: date, json_data: dict) -> XRate:
        base_currency = json_data['baseCurrency'].upper()
        to_currency = json_data['currency'].upper()

        purchase_rate = json_data.get('purchaseRate')
        purchase_rate = float(json_data['purchaseRateNB']) if not purchase_rate else float(purchase_rate)

        sale_rate = json_data.get('saleRate')
        sale_rate = float(json_data['saleRateNB']) if not sale_rate else float(sale_rate)

        return XRate(base_currency, to_currency, purchase_rate, sale_rate, exchange_date)

    @staticmethod
    def rate_aliases():
        return "CHF", "EUR", "GBP", "PLZ", "SEK", "UAH", "USD", "XAU", "CAD"


def get_dates() -> [list[date], None]:
    print(f"Enter dates in format: {date.today()}")

    try:
        start_date = date.fromisoformat(input("start date: "))
        end_date = input("end date: ")
        end_date = start_date if len(end_date) == 0 else date.fromisoformat(end_date)

        if start_date > end_date:
            raise CustomException('the start date is greater than the end date ')

        today = date.today()
        if start_date > today or end_date > today:
            raise CustomException('the date is greater than today ')

    except ValueError:
        print('Invalid input date')
        return
    except CustomException as e:
        print(f"Exception: {e}")
        return

    return [start_date + datetime.timedelta(days=delta) for delta in range((end_date - start_date).days + 1)]


def get_currency() -> [str, None]:
    print(f"Available currencies: {PrivatApi.rate_aliases()}")

    try:
        currency = input("Enter currency: ").upper()

        if currency not in PrivatApi.rate_aliases():
            raise ValueError
    except ValueError:
        print('Invalid input currency')
        return

    return currency


def start():
    dates = get_dates()
    if not dates:
        return

    currency_name = get_currency()
    if not currency_name:
        return

    pb = PrivatApi()
    print(f"Currency {currency_name}:")
    try:
        [print(f"{i.exchange_date}: {i.purchase_rate} / {i.sale_rate}") for i in
         pb.get_currency_rates(currency_name, dates)]
    except CustomException as e:
        print(f"Exception: {e}")


if __name__ == '__main__':
    start()
