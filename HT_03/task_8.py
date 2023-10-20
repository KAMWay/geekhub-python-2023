# Створити цикл від 0 до ... (вводиться користувачем). В циклі створити умову, яка буде виводити поточне значення,
# якщо остача від ділення на 17 дорівнює 0.

[print(i) for i in range(int(input("Input number: "))) if i % 17 == 0]

# This can be realized by the following code (without condition):
#   [print(i) for i in range(0, int(input("Input number: ")), 17)]
