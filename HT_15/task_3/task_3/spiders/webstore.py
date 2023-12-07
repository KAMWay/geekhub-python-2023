from typing import Any

import scrapy
from scrapy import Request
from scrapy.http import Response

from task_3.items import DetailScrapyItem
from task_3.parsers.webstore.parser import WebstoreParser


class WebstoreSpider(scrapy.Spider):
    parser = WebstoreParser()

    name = 'webstore'
    start_urls = 'https://chrome.google.com/webstore/sitemap'

    def parse(self, response: Response, **kwargs: Any):
        print(response.text)

        yield DetailScrapyItem(
            id="gg",
            name="rez.name",
            info="rez.info",
        )


        # results = self.parser.parse_sitemap(response.text)
        # for result in results:
        #     yield Request(
        #         url=result.loc,
        #         callback=self.parse_details_urls,
        #     )
    #
    # def parse_details_urls(self, response: Response):
    #     results = self.parser.parse_details_urls(response.text)
    #     for result in results:
    #         yield Request(
    #             url=result.url,
    #             callback=self.parse_details,
    #         )
    #
    # def parse_details(self, response: Response):
    #     url = response.url
    #     id = url[:url.rfind("/")]
    #     rez = self.parser.parse_detail(response.text)
    #     yield DetailScrapyItem(
    #         id=id,
    #         name=rez.name,
    #         info=rez.info,
    #     )
