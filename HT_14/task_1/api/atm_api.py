from random import randrange

from HT_14.task_1.api.console_api import ConsoleReaderApi
from HT_14.task_1.api.xrate_api import PrivatApi
from HT_14.task_1.model import User, ATMException, Banknote, ATMValidateException, ATM, Transaction
from HT_14.task_1.service import UserService, BanknoteService, UserBalanceService, UserTransactionService


class ATMApi:
    def __init__(self):
        self.__xrate_api = PrivatApi()
        self.__user_service = UserService()
        self.__banknote_service = BanknoteService()
        self.__user_balance_service = UserBalanceService()
        self.__user_transaction_service = UserTransactionService()

    def get_user(self) -> User:
        count = 3
        user = None
        while not user or user.id is None:
            user = ConsoleReaderApi.get_user()
            try:
                exist_user = self.__user_service.get(user.username, user.password)
                if exist_user:
                    return exist_user
                if input(f"User not found. To create '{user.username}' enter 1:") == '1':
                    self.__user_service.save(user)
            except ATMValidateException as e:
                print(f"Validate exception: {e}")

            if not user.id and count > 0:
                count -= 1
                print(f'You have {count + 1} attempts. Try again.')
            elif count <= 0:
                raise ATMException("you could not login")

        return user

    def __save_banknote(self, banknote: Banknote):
        self.__banknote_service.save(banknote)

    def __get_atm_balance(self, atm: ATM) -> int:
        return sum(i.denomination * i.amount for i in self.__banknote_service.get_all(atm.id))

    def __get_amount_banknotes(self, amount: [int, float], atm: ATM) -> int:
        pass

    def __get_bonus_percent(self, user: User, bonus_size: int = 10) -> float:
        if len(self.__user_transaction_service.get_all(user.id)) != 0:
            return 0

        return bonus_size / 100 if not randrange(0, 9, 1) else 0

    def __change_atm_balance(self, amount: [int, float], atm: ATM) -> list[Banknote]:
        if amount == 0 or amount > 0:
            return []

        banknotes = self.__banknote_service.get_all_by_amount(-amount, atm.id)
        self.__banknote_service.update_exist_banknotes(
            [Banknote(i.denomination, -i.amount, i.atm_id) for i in banknotes], atm.id)

        return banknotes

    def __change_user_balance(self, user: User, amount: [int, float], atm: ATM) -> [float, list[Banknote]]:
        user_balance = self.__user_balance_service.get(user.id)

        if amount < 0 and user_balance < -amount:
            raise ATMException('insufficient user funds')

        atm_balance = self.__get_atm_balance(atm)
        if amount < 0 and atm_balance < -amount:
            raise ATMException('insufficient ATM funds')

        min_banknote = min(self.get_available_denomination())
        back_amount = abs(amount % (min_banknote if amount > 0 else -min_banknote))
        amount = amount - (back_amount if amount > 0 else - back_amount)

        if amount == 0:
            return back_amount

        banknotes = self.__change_atm_balance(amount, atm)

        amount += amount * self.__get_bonus_percent(user) if amount > 0 else 0
        user_balance += amount

        self.__user_balance_service.save(user.id, user_balance)
        self.__user_transaction_service.save(Transaction(user.id, None, amount, user_balance))

        return back_amount if amount > 0 else banknotes

    def __get_user_transactions(self, user: User):
        return self.__user_transaction_service.get_all(user.id)

    def get_cmd_result_str(self, user: User, atm: ATM = ATM(1)) -> str:
        command = ConsoleReaderApi.get_command(user.is_admin())
        if command == 0:
            return 'Exit'

        if command == 1:
            return f'Total user deposit: {self.__user_balance_service.get(user.id)}'

        if command == 2:
            return f'Total ATM deposit: {self.__get_atm_balance(atm)}'

        if command == 3 or command == 4:
            amount = ConsoleReaderApi.get_amount()
            back_amount = self.__change_user_balance(user, (amount if command == 3 else -amount), atm)
            if isinstance(back_amount, float):
                return 'Done' if back_amount == 0 else f'Return {round(back_amount, 2)}'
            if isinstance(back_amount, list):
                return ', '.join(
                    f"{i}" for i in back_amount) + f" Total: {sum(i.denomination * i.amount for i in back_amount)}"

        if command == 5:
            str_generator = ('Date {} Amount: {}'.format(item.dt, item.amount)
                             for item in self.__get_user_transactions(user))
            return '\n'.join(str_generator)

        if command == 6:
            rates = self.__xrate_api._get_rates()
            str_generator = (f"{rate.to_currency} {rate.buy_rate}/{rate.sale_rate}" for rate in rates)
            return '\n'.join(str_generator)

        if user.is_admin() and command == 7:
            banknote = ConsoleReaderApi.get_banknote_amount(self.get_available_denomination())
            banknote.atm_id = atm.id
            self.__save_banknote(banknote)
            return 'Done'

        if user.is_admin() and command == 8:
            str_generator = (f"Denomination {item.denomination} Amount: {item.amount}"
                             for item in self.__banknote_service.get_all())
            return '\n'.join(str_generator)

    @staticmethod
    def get_available_denomination() -> tuple:
        return 10, 20, 50, 100, 200, 500, 1000
