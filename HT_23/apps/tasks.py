import logging

from apps.celery import celery_app as app
from apps.products.models import ScrapyTask
from apps.scraper.models import ScrapingTask

logger = logging.getLogger('django')


# @app.task(name='ht_23')
# def every_5_seconds(**kwargs):
#     logger.info(f'Start every_5_seconds')
#     return 'every_5_seconds'


# @app.task(name='ht_23')
@app.task
def start_scraping(**kwargs):
    logger.info(f'Start scrapingscrapingscraping')
    # return 'scrapingscrapingscrapingscrapingscraping'
    scrapy_task = ScrapyTask.objects.get(id=kwargs.get('scrapy_task_id'))
    ids = set(item.strip() for item in scrapy_task.ids_str.split(sep=','))
    task = ScrapingTask(ids)
    task.run()
    scrapy_task.delete()
    # return 'Jrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'
