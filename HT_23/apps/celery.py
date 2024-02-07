import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.main')

app = Celery('apps',
             # include=['apps.tasks', ]
             )

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     "every_3_seconds": {
#         "task": "every_5_second",
#         "schedule": crontab(second="3")
#     }
# }
