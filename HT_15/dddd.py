from datetime import datetime

import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    response = requests.get('https://chrome.google.com/webstore/sitemap')

    soup = BeautifulSoup(response.text, 'lxml')

    sitemaps = soup.select('sitemap')
    [print(f'{i.loc.text} {datetime.strptime(i.lastmod.text, "%Y-%m-%dT%H:%M:%S.%fZ")}') for i in sitemaps]
