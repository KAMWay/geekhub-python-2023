from django.core.management.base import BaseCommand, CommandError

from apps.products.models import ScrapyTask

from apps.scraper.models import ScrapingTask


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("task_id", nargs="+", type=int)

    def handle(self, *args, **options):
        try:
            task_id = options['task_id'][0]
            scrapy_task = ScrapyTask.objects.get(id=task_id)
            ids = set(item.strip() for item in scrapy_task.ids_str.split(sep=','))

            task = ScrapingTask(ids)
            task.run()

            scrapy_task.delete()
        except ScrapyTask.DoesNotExist:
            raise CommandError(f'ScrapyTask "{task_id}" does not exist')
        except ValueError:
            raise CommandError('Invalid scrapy_task argument')
