# 1. Додайте до банкомату меню отримання поточного курсу валют за допомогою requests
# (можна використати відкрите API ПриватБанку)
from HT_14.task_1.api.atm_api import ATMApi
from HT_14.task_1.model import ATMException


def start():
    atm_service = ATMApi()
    user = None
    try:
        user = atm_service.get_user()
    except ATMException as e:
        print(f'Login exception: {e}')

    while user:
        try:
            print('- - - - - - - - - - - -')
            rez = atm_service.get_command_result(user)
            print(rez)
            print('- - - - - - - - - - - -')
            if rez == 'Exit':
                break
        except ATMException as e:
            print(f'Command exception: {e}')

    print('Program complete')


if __name__ == '__main__':
    start()
