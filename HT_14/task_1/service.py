from HT_14.task_1.model import ATMValidateException, User, Transaction, Banknote, ATMException
from HT_14.task_1.repository import UserRepository, UserBalanceRepository, UserTransactionRepository, BanknoteRepository


class UserService:
    def __init__(self):
        self.__user_repository = UserRepository()

    def __validate(self, username: str, password: str, is_new: bool = False):
        if not username or not password:
            raise ATMValidateException("username and password can't be empty")
        if is_new and self.__user_repository.get_by_username(username):
            raise ATMValidateException(f"can't used exist username '{username}'")

    def get(self, username: str, password: str) -> User:
        self.__validate(username, password)
        user = self.__user_repository.get_by_username(username)
        return None if not user or user.password != password else user

    def save(self, user: User):
        self.__validate(user.username, user.password, user.is_new())
        self.__user_repository.insert(user)


class UserBalanceService:
    def __init__(self):
        self.__user_balance_repository = UserBalanceRepository()

    def get(self, user: int) -> float:
        user_balance = self.__user_balance_repository.get_by_user_id(user)
        return user_balance if user_balance else 0

    def save(self, user: int, amount: [int, float]):
        if self.__user_balance_repository.get_by_user_id(user):
            self.__user_balance_repository.update(user, amount)
        else:
            self.__user_balance_repository.insert(user, amount)


class UserTransactionService:
    def __init__(self):
        self.__user_transaction_repository = UserTransactionRepository()

    def get_all(self, user: int) -> list[Transaction]:
        return self.__user_transaction_repository.get_all_by_user_id(user)

    def save(self, transaction: Transaction):
        self.__user_transaction_repository.insert(transaction)


class BanknoteService:
    def __init__(self):
        self.__banknote_repository = BanknoteRepository()

    def save(self, banknote: Banknote):
        if banknote.amount < 0:
            raise ATMException(f"can't save negative amount of banknote")

        if self.__banknote_repository.get_by_denomination(banknote.denomination):
            self.__banknote_repository.update(banknote)
        else:
            self.__banknote_repository.insert(banknote)

    def get_all(self, atm_id: int = 1) -> list[Banknote]:
        return self.__banknote_repository.get_all_by_atm_id(atm_id)

    def __get_banknote_by_denomination(self, denomination: int, banknotes: list[Banknote]) -> Banknote:
        return next(i for i in banknotes if i.denomination == denomination)

    def update_exist_banknotes(self, change_banknotes: list[Banknote], atm_id: int = 1):
        if not change_banknotes or not len(change_banknotes):
            return

        exist_banknotes = self.get_all(atm_id)
        upd_banknotes = []
        ins_banknotes = []
        for cur in change_banknotes:
            if cur.amount == 0:
                continue

            exist_banknote = self.__get_banknote_by_denomination(cur.denomination, exist_banknotes)
            if exist_banknote:
                cur.amount += exist_banknote.amount
                upd_banknotes.append(cur)
            elif cur.amount > 0:
                ins_banknotes.append(cur)

        if any(i for i in upd_banknotes if i.amount < 0) or any(i for i in ins_banknotes if i.amount < 0):
            raise ATMException(f"can't save negative amount of banknotes")

        if len(upd_banknotes):
            self.__banknote_repository.update_all(upd_banknotes)
        if len(ins_banknotes):
            self.__banknote_repository.insert_all(ins_banknotes)

    def get_all_by_amount(self, amount: int, atm_id: int = 1) -> list[Banknote]:
        if amount <= 0:
            raise ATMException("can't get banknote combinations for negative amount")

        try:
            banknotes = self.__get_combinations(self.get_all(atm_id), amount)
            if len(banknotes) == 0:
                raise ATMException

            return [i for i in banknotes if i.amount != 0]
        except Exception:
            raise ATMException("can't get banknote combinations")

    def __get_combinations(self, banknotes: list[Banknote], amount: int,
                           combinations: list[Banknote] = None, position: int = 0) -> list[Banknote]:
        banknotes.sort(key=lambda x: x.denomination, reverse=True)
        if not combinations:
            combinations = [Banknote(i.denomination, 0) for i in banknotes]

        value = sum([i.denomination * i.amount for i in combinations])

        if value < amount:
            for i in range(position, len(banknotes)):
                if banknotes[i].amount > combinations[i].amount:
                    new_variation = [i for i in combinations]
                    new_variation[i] = Banknote(new_variation[i].denomination, new_variation[i].amount + 1)
                    new_list = self.__get_combinations(banknotes, amount, new_variation, i)
                    if new_list:
                        return new_list
        elif value == amount:
            return combinations
