# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import logging
from pathlib import Path

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Task3ScrapyPipeline:
    results_dir = 'results'

    DIR = Path(Path.cwd(), results_dir)

    def __save_to_csv(self, item_dict: dict, *, delimiter: str = '|'):
        file = Path(self.DIR, f'{item_dict["id"]}.csv')
        fieldnames = item_dict.keys()
        with open(file, "w", newline='', encoding='UTF-8') as f:
            writer = csv.DictWriter(f, delimiter=delimiter, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(item_dict)

    def open_spider(self, spider):
        self.DIR.mkdir(parents=True, exist_ok=True)

    def process_item(self, item, spider):
        try:
            self.__save_to_csv(item)
            spider.log(f'{item["id"]} processed', logging.INFO)
        except Exception:
            spider.log(f'invalid save {item["id"]}', logging.ERROR)

        return item
