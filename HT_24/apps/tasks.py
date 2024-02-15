import logging

from apps.celery import celery_app as app
from apps.scraper.models import ScrapingTask

logger = logging.getLogger('django')


@app.task(name='scraping_products_items')
def scraping_items(**kwargs):
    ids = kwargs.get('ids')
    task = ScrapingTask(ids)
    task.run()
