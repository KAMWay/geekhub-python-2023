from bs4 import BeautifulSoup

from task_3_scrapy.parsers.webstore.dataclasses import DetailUrl, DetailItem


class WebstoreParser:
    def parse_sitemap(self, response_txt: str) -> list[DetailUrl]:
        soup = BeautifulSoup(response_txt, 'lxml')
        return [
            DetailUrl(
                loc=sitemap.loc.text,
                lastmod=sitemap.lastmod.text,
            )
            for sitemap in soup.select('sitemap')
        ]

    def parse_details_urls(self, response_txt: str) -> list[DetailUrl]:
        soup = BeautifulSoup(response_txt, 'lxml')
        return [
            DetailUrl(
                loc=sitemap.loc.text,
                lastmod=sitemap.lastmod.text,
            )
            for sitemap in soup.select('url')
        ]

    def parse_detail(self, response_txt: str) -> DetailItem:
        soup = BeautifulSoup(response_txt, 'lxml')
        return DetailItem(
            name=soup.select_one('h1.Pa2dE').text,
            info=soup.select_one('div.uORbKe').text,
        )
