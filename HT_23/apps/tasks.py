import logging

from apps.celery import celery_app as app
from apps.scraper.models import ScrapingTask

logger = logging.getLogger('django')


@app.task(name='scraping_products_items')
def scraping_items(**kwargs):
    # scrapy_task = ScrapyTask.objects.get(id=kwargs.get('scrapy_task_id'))
    # ids = set(item.strip() for item in scrapy_task.ids_str.split(sep=','))

    ids = kwargs.get('ids')
    task = ScrapingTask(ids)
    task.run()
    # scrapy_task.delete()
