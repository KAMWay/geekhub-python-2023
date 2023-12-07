import logging
from datetime import datetime

from bs4 import BeautifulSoup
from scrapy.utils import log

from task_3.parsers.webstore.dataclasses import SitemapItems, DetailUrl, DetailItem


class WebstoreParser:
    def parse_sitemap(self, response_txt: str) -> list[SitemapItems]:
        soup = BeautifulSoup(response_txt, 'lxml')

        return [
            SitemapItems(
                loc=sitemap.loc.text,
                lastmod=datetime.strptime(sitemap.lastmod.text, "%Y-%m-%dT%H:%M:%S.%fZ"),
            )
            for sitemap in soup.select('sitemap')
        ]

    def parse_details_urls(self, response_txt: str) -> list[DetailUrl]:
        items = response_txt.split(' ')

        if len(items) % 2 != 0:
            log.logger('invalid parse sitemap', logging.ERROR)
            return []

        return [
            DetailUrl(
                url=items[i].strip(),
                period_str=items[i + 1].strip(),
            )
            for i in range(0, len(items), 2)
        ]

    def parse_detail(self, response_txt: str) -> DetailItem:
        soup = BeautifulSoup(response_txt, 'lxml')
        return DetailItem(
            name=soup.h1.text,
            info=soup.select_one('div.uORbKe').text,
        )
