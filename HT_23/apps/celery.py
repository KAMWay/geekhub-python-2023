import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.main')

celery_app = Celery('apps')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    "update_every_5_seconds": {
        "task": "every_5_seconds",
        "schedule": timedelta(seconds=5),
    }
}
