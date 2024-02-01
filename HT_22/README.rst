Home task 22
========

1. Install requirements::

    pip install -r ./requirements/production.txt


2. Migrate Database::

    python manage.py migrate

3. Run Django server::

    python manage.py runserver


Task
---------------------

Базуючись на попередній ДЗ, реалізувати наступний функціонал:
Додавання до корзини, зміну кількості, очищення корзини або видалення одного продукта з неї зробити з використанням ajax запитів.

Корисні посилання:
https://www.geeksforgeeks.org/how-to-make-ajax-call-from-javascript/
https://developer.mozilla.org/en-US/docs/Web/Guide/AJAX/Getting_Started