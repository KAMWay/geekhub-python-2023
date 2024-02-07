from apps.celery import app
from apps.products.models import ScrapyTask
from apps.scraper.models import ScrapingTask


@app.task(name='do_scraping')
def scraping(**kwargs):
    return 'Jrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'
    # scrapy_task = ScrapyTask.objects.get(id=kwargs.get('scrapy_task_id'))
    # ids = set(item.strip() for item in scrapy_task.ids_str.split(sep=','))
    # task = ScrapingTask(ids)
    # task.run()
    # scrapy_task.delete()
    # return 'Jrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'
