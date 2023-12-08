# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class Task3ScrapyItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass


class DetailScrapyItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    info = scrapy.Field()

    def dict(self):
        return self.__dict__
