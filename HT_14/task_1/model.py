from datetime import datetime


class ATMException(Exception):
    pass


class ATMValidateException(ATMException):
    pass


class User:
    def __init__(self, user_id: [int, None], username: str, password: str):
        self.__id = user_id
        self.__username = username
        self.__password = password

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, _id: int):
        self.__id = _id

    @property
    def username(self) -> str:
        return self.__username

    @username.setter
    def username(self, username: str):
        self.__username = username

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, password: str):
        self.__password = password

    def is_new(self):
        return self.id is None

    def is_admin(self):
        return self.id == 1


class ATM:
    def __init__(self, _id: int = 1, info: str = ""):
        self.__id = _id
        self.__info = info

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, _id: int):
        self.__id = _id

    @property
    def info(self) -> str:
        return self.__info

    @info.setter
    def info(self, info: str):
        self.__info = info


class Banknote:
    def __init__(self, denomination: int, amount: int, atm_id: int = 1):
        self.__denomination = denomination
        self.__amount = amount
        self.__atm_id = atm_id

    @property
    def atm_id(self) -> int:
        return self.__atm_id

    @atm_id.setter
    def atm_id(self, atm_id: int):
        self.__atm_id = atm_id

    @property
    def denomination(self) -> int:
        return self.__denomination

    @denomination.setter
    def denomination(self, denomination: int):
        self.__denomination = denomination

    @property
    def amount(self) -> int:
        return self.__amount

    @amount.setter
    def amount(self, amount: int):
        self.__amount = amount

    def __str__(self):
        return f"{self.__amount}x{self.__denomination}"


class Transaction:
    def __init__(self, user_id: int, dt: [datetime, None], amount: [float, int], balance: [float, int]):
        dt = datetime.now() if not dt else dt
        self.__user_id = user_id
        self.__dt = dt
        self.__amount = amount
        self.__balance = balance

    @property
    def user_id(self) -> int:
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id: int):
        self.__user_id = user_id

    @property
    def dt(self) -> datetime:
        return self.__dt

    @dt.setter
    def dt(self, dt: datetime):
        self.__dt = dt

    @property
    def amount(self) -> float:
        return self.__amount

    @amount.setter
    def amount(self, amount: float):
        self.__amount = amount

    @property
    def balance(self) -> float:
        return self.__balance

    @balance.setter
    def balance(self, balance: float):
        self.__balance = balance


class XRate:
    def __init__(self, base_currency: str, to_currency: str, buy_rate: float, sale_rate: float,
                 updated: datetime = None):
        updated = datetime.now() if not updated else updated
        self.__base_currency = base_currency
        self.__to_currency = to_currency
        self.__buy_rate = buy_rate
        self.__sale_rate = sale_rate
        self.__updated = updated

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
    def buy_rate(self) -> float:
        return self.__buy_rate

    @buy_rate.setter
    def buy_rate(self, buy_rate: float):
        self.__buy_rate = buy_rate

    @property
    def sale_rate(self) -> float:
        return self.__sale_rate

    @sale_rate.setter
    def sale_rate(self, sale_rate: float):
        self.__sale_rate = sale_rate

    @property
    def updated(self) -> datetime:
        return self.__updated

    @updated.setter
    def updated(self, updated: datetime):
        self.__updated = updated

    def __str__(self):
        return (f"[{self.__base_currency}=>{self.__to_currency}] "
                f"[{self.__buy_rate}, {self.__sale_rate}] "
                f"updated: {self.__updated}")
