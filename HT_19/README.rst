Home task 19
========

1. Install requirements::

    pip install -r ./requirements/production.txt


2. Migrate Database::

    python manage.py migrate

3. Run Django server::

    python manage.py runserver


Task
---------------------

Додати сторінку корзини та імплементувати додавання продукта до корзини, зміну кількості продукта (перевіряти на від'ємне значення як введеного значення, так і отриманої кількості), видалення одного продукта, очищення всієї корзини.