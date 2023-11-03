# Створіть функцію, всередині якої будуть записано список із п'яти користувачів (ім'я та пароль). Функція повинна
# приймати три аргументи: два - обов'язкових (<username> та <password>) і третій - необов'язковий параметр <silent>
# (значення за замовчуванням - <False>).
# Логіка наступна:
#     якщо введено коректну пару ім'я/пароль - вертається True;
#     якщо введено неправильну пару ім'я/пароль:
#         якщо silent == True - функція вертає False
#         якщо silent == False -породжується виключення LoginException (його також треба створити =))

class LoginException(Exception):
    pass


def is_exist(username: str, psw: str, silent: bool = False) -> bool:
    _users = [{'user1': 'psw123456'}, {'user2': 'psw1234567'},
              {'user3': 'psw12345678'}, {'user4': 'psw123456'},
              {'user5': 'psw12345'}, ]

    if not username or not psw:
        return False

    if any(filter(lambda i: i.get(username) == psw, _users)):
        return True

    if silent:
        return False
    else:
        raise LoginException('login fail')


if __name__ == '__main__':
    print(is_exist('user1', 'psw12', True))
    print(is_exist('user1', 'psw123456', ))
    print(is_exist('user5', 'psw12345678'))
