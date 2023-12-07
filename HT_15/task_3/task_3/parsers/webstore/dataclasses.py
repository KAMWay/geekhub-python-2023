from dataclasses import dataclass
from datetime import datetime


@dataclass
class SitemapItems:
    loc: str
    lastmod: datetime


@dataclass
class DetailUrl:
    url: str
    period_str: str


@dataclass
class DetailItem:
    name: str
    info: str
