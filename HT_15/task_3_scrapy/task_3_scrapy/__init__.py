# 3. Використовуючи Scrapy, заходите на "https://chrome.google.com/webstore/sitemap", переходите на кожен лінк
# з тегів <loc>, з кожного лінка берете посилання на сторінки екстеншенів, парсите їх і зберігаєте в CSV файл ID,
# назву та короткий опис кожного екстеншена (пошукайте уважно де його можна взяти)

from scrapy.cmdline import execute

execute("scrapy crawl webstore".split())
