# 3. На основі попередньої функції (скопіюйте кусок коду) створити наступний скрипт:
#    а) створити список із парами ім'я/пароль різноманітних видів (орієнтуйтесь по правилам своєї функції) - як валідні, так і ні;
#    б) створити цикл, який пройдеться по цьому циклу і, користуючись валідатором, перевірить ці дані і надрукує для кожної пари значень відповідне повідомлення, наприклад:
#       Name: vasya
#       Password: wasd
#       Status: password must have at least one digit
#       -----
#       Name: vasya
#       Password: vasyapupkin2000
#       Status: OK
#    P.S. Не забудьте використати блок try/except ;)

class ValidateException(Exception):
    pass


def is_valid_username_and_psw(username: str, psw: str) -> bool:
    if not username or not psw:
        raise ValidateException("username and password can't be empty")

    if 3 > len(username) or len(username) > 50:
        raise ValidateException('username length must be in the range [3..50]')

    if len(psw) < 8 or not any(ch.isdigit() for ch in psw):
        raise ValidateException('password length must be more than 8 and contain digit')

    if all(map(lambda i: i.isdigit() or i.isalpha(), username)):
        return True
    else:
        raise ValidateException('username must be an alphabetic and digit')


def print_login_validate(users_list: list[dict]):
    for user in users_list:
        for k, v in user.items():
            print(f'Name: {k}')
            print(f'Password: {v}')
            print('Status: ', end='')
            try:
                print('OK' if is_valid_username_and_psw(k, v) else 'FAIL')
            except ValidateException as e:
                print(e)
            finally:
                print('-----')


if __name__ == '__main__':
    users = [{'user1': 'psw123456'}, {'user1&': 'psw123456'},
             {'user1': 'pswfghfhfhf'}, {'user1': 'psw 2'},
             {'': ''}, {None: None},
             {'user1': 'psw123456'}, {'user5': 'psw12345678'}]

    print_login_validate(users)
