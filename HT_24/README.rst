Home task 24
========

1. Install requirements::

    pip install -r ./requirements/development.txt

2. Migrate Database::

    python manage.py migrate

3. Creating environment file .env file by sample::

    DEBUG=on
    SECRET_KEY=your-secret-key

    CELERY_BROKER_URL=your-celery-broker-url
    CELERY_RESULT_BACKEND=your-celery-result-backend-url

4. Run with Django::

    python manage.py runserver
    celery -A apps worker -l INFO -P solo

5. or run with Docker::

    docker-compose up --build

Task
---------------------

Додати тести на АПІ ендпоінти, які ви додавали в HT 21-22.