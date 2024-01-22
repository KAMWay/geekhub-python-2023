from django.core.management.base import BaseCommand, CommandError

from apps.product.models import ScrapyTask

from scraper.models import ScrapingTask


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("task_id", nargs="+", type=int)

    def handle(self, *args, **options):
        try:
            task_id = options['task_id'][0]
            ids_str = ScrapyTask.objects.get(id=task_id).ids_str
            ids = set(item.strip() for item in ids_str.split(sep=','))

            task = ScrapingTask(ids)
            task.run()
        except ScrapyTask.DoesNotExist:
            raise CommandError(f'ScrapyTask "{task_id}" does not exist')
        except ValueError:
            raise CommandError('Invalid scrapy_task argument')
