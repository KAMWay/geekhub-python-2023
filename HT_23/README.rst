Home task 23
========

1. Install requirements::

    pip install -r ./requirements/production.txt


2. Migrate Database::

    python manage.py migrate

3. Run Django server::

    python manage.py runserver


Task
---------------------

Доробити процес скрейпінгу нових продуктів, використовуючи в якості скрейпера запроси з модулем requests, а багатопотоковості скрейпінга досягнути використанням Celery завдань.

Корисні посилання:

https://docs.celeryq.dev/en/stable/getting-started/introduction.html

https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#django-first-steps