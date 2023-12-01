from HT_14.task_1.model import User, ATMException, Banknote


class ConsoleReaderApi:
    @staticmethod
    def get_user() -> User:
        print()
        print('----Please Sign In/Up----')
        username = input('Enter user name: ')
        password = input('Enter password: ')
        return User(None, username, password)

    @staticmethod
    def get_amount() -> float:
        try:
            amount = float(input('Input amount: '))
            if amount <= 0:
                raise ValueError
            return amount
        except ValueError:
            raise ATMException('incorrect input amount')

    @staticmethod
    def get_banknote_amount(available_denomination: tuple) -> Banknote:
        try:
            banknote = int(input('Input banknotes denomination [10, 20, 50, 100, 200, 500, 1000]: '))
            if banknote not in available_denomination:
                raise ValueError

            amount = int(input('Input amount: '))
            if amount < 0:
                raise ValueError

            return Banknote(banknote, amount)
        except ValueError:
            raise ATMException('incorrect input banknotes')

    @staticmethod
    def get_command(is_admin: bool = False, min_cmd_number: int = 6, max_cmd_number: int = 8) -> int:
        count_commands = max_cmd_number if is_admin else min_cmd_number
        while True:
            print()
            print('----Available ATM commands----')
            print('1. User balance')
            print('2. ATM balance')
            print('3. Top-up user balance')
            print('4. Withdrawing money')
            print('5. Transaction history')
            print('6. Exchange rate')
            print('0. Exit')

            if is_admin:
                print('7. Admin: top-up banknotes')
                print('8. Admin: available banknotes')

            print('------------------------')
            try:
                number = int(input(f"Enter command number [1..{count_commands}]:"))
                print('- - - - - - - - - - - -')
                if 0 <= number <= count_commands:
                    return number
                raise ValueError()
            except ValueError:
                print('Incorrect input. Try again.')
