from dataclasses import dataclass


@dataclass
class DetailUrl:
    loc: str
    lastmod: str


@dataclass
class DetailItem:
    name: str
    info: str

    def dict(self):
        return self.__dict__
