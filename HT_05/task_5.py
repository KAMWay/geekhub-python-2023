# Ну і традиційно - калькулятор :slightly_smiling_face: Повинна бути 1 ф-цiя, яка б приймала 3 аргументи - один з яких
# операцiя, яку зробити!
# Аргументи брати від юзера (можна по одному - 2, окремо +, окремо 2; можна всі разом - типу 1 + 2).
# Операції що мають бути присутні: +, -, *, /, %, //, **.
# Не забудьте протестувати з різними значеннями на предмет помилок!

def to_number(value):
    try:
        try:
            return int(value)
        except ValueError:
            return float(value)
    except ValueError:
        return None


def number_calculate(operator, a, b):
    func = get_function(operator)
    try:
        return get_result(func, a, b)
    except ZeroDivisionError:
        return 'Division by Zero'
    except ArithmeticError:
        return 'Arithmetic error'


def get_function(operator: str):
    if operator == '+':
        return lambda a, b: a + b
    elif operator == '-':
        return lambda a, b: a - b
    elif operator == '*':
        return lambda a, b: a * b
    elif operator == '/':
        return lambda a, b: a / b
    elif operator == '%':
        return lambda a, b: a % b
    elif operator == '//':
        return lambda a, b: a // b
    elif operator == '**':
        return lambda a, b: a ** b
    else:
        return None


def get_result(func, a, b):
    if func is not None and is_valid_args(a, b):
        return func(a, b)


# Can be realized with Python func eval()
def get_eval_result(func, a, b):
    if is_valid_func(func, a, b):
        return eval(f'{a} {func} {b}')


def is_valid_func(func, a, b):
    return is_access_function(func) and to_number(a) is not None and to_number(b) is not None


def is_access_function(func):
    access_function = ('+', '-', '*', '/', '%', '//', '**')
    return func is not None and func in access_function


def is_valid_args(a, b):
    return to_number(a) is not None and to_number(b) is not None


def parse_func_operator(items_str: str):
    _items = list(filter(is_access_function, items_str.split(' ')[:3]))
    if len(_items) == 1:
        return _items[0]
    else:
        return None


def parse_func_args(items_str: str):
    _items = list(filter(lambda i: i is not None, map(to_number, items_str.split(' ')[:3])))
    if len(_items) == 2:
        return _items
    else:
        return None


def get_func_and_args_from_console():
    str_line = input("Enter operation line with digits (e.g.  a + b): ").strip()

    args = None
    operator = None
    while args is None or operator is None:
        if operator is None:
            operator = parse_func_operator(str_line)
        if args is None:
            args = parse_func_args(str_line)
        if len(str_line.split()) < 3:
            str_line += ' ' + input().strip()
        else:
            return args, operator


if __name__ == '__main__':
    func_args, func_operator = get_func_and_args_from_console()

    if func_args is not None and func_operator is not None:
        rez = number_calculate(a=func_args[0], b=func_args[1], operator=func_operator)
        print(f'The result of the operation: {rez}')
    else:
        print("Can't parser input string to args and operation")
