import scrapy
from scrapy import Request
from scrapy.http import Response

from task_3_scrapy.items import DetailScrapyItem
from task_3_scrapy.parsers.webstore.parser import WebstoreParser


class WebstoreSpider(scrapy.Spider):
    name = "webstore"
    allowed_domains = ["google.com"]
    start_urls = ["https://chrome.google.com/webstore/sitemap"]
    parser = WebstoreParser()

    def parse(self, response, **kwargs):
        results = self.parser.parse_sitemap(response.text)
        for result in results:
            yield Request(
                url=result.loc,
                callback=self.parse_details_urls,
            )

    def parse_details_urls(self, response: Response):
        results = self.parser.parse_details_urls(response.text)
        for result in results:
            yield Request(
                url=result.loc,
                callback=self.parse_details,
            )

    def parse_details(self, response: Response):
        url = response.url
        _id = url[url.rfind("/") + 1:]
        rez = self.parser.parse_detail(response.text)
        yield DetailScrapyItem(
            id=_id,
            name=rez.name,
            info=rez.info,
        )
