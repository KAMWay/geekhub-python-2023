# Створіть функцію для валідації пари ім'я/пароль за наступними правилами:
#    - ім'я повинно бути не меншим за 3 символа і не більшим за 50;
#    - пароль повинен бути не меншим за 8 символів і повинен мати хоча б одну
#    цифру;
#    - якесь власне додаткове правило :)
#    Якщо якийсь із параментів не відповідає вимогам - породити виключення із відповідним текстом.

class ValidateException(Exception):
    pass


def is_valid_login(username: str, psw: str) -> bool:
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


if __name__ == '__main__':

    print(is_valid_login('user1', 'psw123456'))

    try:
        print(is_valid_login('user1&', 'psw123456'))
    except ValidateException as e:
        print(e)

    try:
        print(is_valid_login('user1', 'pswfghfhfhf'))
    except ValidateException as e:
        print(e)