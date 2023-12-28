# @background(schedule=60)
# def demo_task(message):
#     logger.debug('demo_task. message={0}'.format(message))
#
#
# import subprocess
#
# process = subprocess.Popen(['python', 'manage.py','process_tasks'], stdout=subprocess.PIPE, stderr=subprocess.PIPE
import json
from urllib.parse import urljoin

import requests
from .models import Product


class ScrapingTask:
    DETAIL_URL = 'https://www.sears.com/api/sal/v3/products/details/'

    HEADERS = {
        'authority': 'www.sears.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6,zh-TW;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'authorization': 'SEARS',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        # 'cookie': 'initialTrafficSource=utmcsr=(direct)|utmcmd=(none)|utmccn=(not set); _gcl_au=1.1.646852101.1702026308; _fbp=fb.1.1702026315636.506290981; GSIDNqXoacKY53MN=ed62baf7-4ff8-4894-9c46-2f3047cfd5de; STSID974004=69b6980a-38f8-4f31-af7b-96af49a5d17b; _pbjs_userid_consent_data=3524755945110770; cookie=5dbe6759-b2cb-4bc2-ad57-78d2196a8570; cookie_cst=zix7LPQsHA%3D%3D; _lc2_fpi=ec742730c587--01hh4at14tfxka7s4j9j11z5a6; _lc2_fpi_meta={%22w%22:1702026347675}; __qca=P0-564974280-1702026348274; __gsas=ID=403d77417479d777:T=1702026540:RT=1702026540:S=ALNI_MadWXXenWbceoDgmE8yDGI3R6z2HQ; ftr_ncd=6; ftr_blst_1h=1703674191355; _gid=GA1.2.2069085897.1703674198; zipCode=10101; city=New York; state=NY; __utmzzses=1; ltkSubscriber-Footer=eyJsdGtDaGFubmVsIjoiZW1haWwiLCJsdGtUcmlnZ2VyIjoibG9hZCJ9; _clck=10k7sd1%7C2%7Cfhw%7C0%7C1437; _vuid=808000d4-2255-494b-8759-0d02c4bda07f; _li_dcdm_c=.sears.com; _li_ss=Cn0KBQgKEOkWCgYIpAEQ6hYKBgjdARDpFgoFCAYQ6hYKBQgJEOoWCgYI4QEQ6RYKBgiBARDpFgoFCAwQ7xYKBgiiARDoFgoJCP____8HEPQWCgUICxDpFgoGCIsBEOoWCgYIiQEQ6hYKBgilARDpFgoGCNIBEOgWCgUIfhDqFg; irp=dcca259a-a744-4a54-89fe-17eda8a45a27|qxBvninnEBA0SRIFUxWPQaZojmDm55VKtKgnmMFHQBA%3D|G|66e3137a-0800-4a46-8526-804ca88f5a45|0|NO_SESSION_TOKEN_COOKIE; __pr.3q8y1p=c2gJFiIIrg; __cf_bm=b_GyTKFYM7k6dz4CkJQ3CPSVAew1uPnGPlTqL5rLdsU-1703677268-1-ASGdoh0TL5kj8h6GacwKSDpGQKelh5G5fSYYmjp/oAsjTBKqUoP9+JDoXKIIMUPAW/NQF9s2kD4F0Qet3RHx6cttOc4u5nezNz59B7S11CFQ; cf_clearance=6AzyQp5SFvXHd71isiYwop.kkjbX4hT1gk30_iz.v7k-1703677280-0-2-92b4b8c9.f92401a7.5fb2d974-0.2.1703677280; __gads=ID=a1c650b5907403d3:T=1702026341:RT=1703677872:S=ALNI_MZtrjIt-lXdcP3UGhItOG4Kj_XoHQ; OptanonAlertBoxClosed=2023-12-27T11:51:54.859Z; OptanonConsent=isIABGlobal=false&datestamp=Wed+Dec+27+2023+13%3A51%3A55+GMT%2B0200+(%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202209.1.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CSPD_BG%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=UA%3B12; forterToken=96d58eacdac4450db231afd6bb231d3b_1703677914128_16032_UDF43-m4_13ck; _ga=GA1.1.10246372.1702026284; ltkpopup-session-depth=3-8; _li_ss_meta={%22w%22:1703677977486%2C%22e%22:1706269977486}; cto_bundle=s-bUa18xdWt4V2xrTWVhUFdFMnE5THFEcGJWMEpaTXREbVp1Q2MlMkZ2SkwwOW4zbHBGUVNzZWY4ejhXYTlSaXdvaWZkbVpya3RiaFJEdkpITUtRJTJCd285eTQxaXlJWjlYS3JmJTJGYlgyMTN1U0twSVFxNFIwVUFXM25iem0lMkJXelRMTGJUVVNldEFpbFk3cSUyQjdoTGtHMDNwNiUyQkxNUXclM0QlM0Q; cto_bidid=7vTTDV9iQWxVdG56bjE4amVWZHZJV1pXQWVySnMlMkZQJTJCajExWjBjR2F3bW9HR3lodVFoTzlUeHNPemFtS0lLUjdpUWtrbkJHckgweGlKTHpENDJNS2ZHTW9NJTJGWFZhVWdjUSUyQnVBd3dVZHN0MkhubGtNJTNE; _clsk=4s9uwr%7C1703678110210%7C15%7C1%7Co.clarity.ms%2Fcollect; _uetsid=b4d00ce0a4a511eebcc8e58fd0e30bc8; _uetvid=e680295095a811eea738ad144003f94f; _ga_L7QE48HF7H=GS1.1.1703677268.6.1.1703678110.44.0.0',
        'pragma': 'no-cache',
        # 'referer': 'https://www.sears.com/kenmore-60492-18-cu-ft-top-freezer/p-A109915280',
        # 'referer': 'https://www.sears.com',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    PARAMS = {
        'storeName': 'Sears',
        'memberStatus': 'G',
        'zipCode': '10101',
    }

    def start(self, product_id: str):
        response = requests.get(urljoin(self.DETAIL_URL, product_id), params=self.PARAMS, headers=self.HEADERS, )
        response.raise_for_status()

        if json.loads(response.text).get('meetExpertHier') is None:
            raise Exception(f'product by id {product_id} does not exist')

        product_dict = json.loads(response.text)['productDetail']['softhardProductdetails'][0]
        product = self.parse_product(product_dict)
        product.save()

    def parse_product(self, product_dict: dict) -> Product:
        url = product_dict.get('seoUrl')
        return Product(
            id=self.__parse_id(url),

            brand_name=product_dict.get('brandName'),
            name=product_dict.get('descriptionName'),
            main_image_url=product_dict.get('mainImageUrl'),
            description=product_dict.get('shortDescription'),
            url=url,

            regular_price=self.__to_float_value(product_dict.get('regularPrice')),
            sale_price=self.__to_float_value(product_dict.get('salePrice')),

            default_seller_id=product_dict.get('defaultSeller').get('sellerId'),
            store_id=self.__to_int_value(product_dict.get('storeId')),
        )

    def __parse_id(self, url: str):
        start_id = url.rfind('p-A')
        start_id = (start_id + 2) if start_id >= 0 else 0

        end_id = url.find('?', start_id)
        end_id = len(url) if end_id < 0 else end_id

        return url[start_id:end_id]

    def __to_float_value(self, value: str):
        try:
            return float(value)
        except TypeError:
            return 0

    def __to_int_value(self, value: str):
        try:
            return int(value)
        except TypeError:
            return 0


def run(product_id: str):
    task = ScrapingTask()
    try:
        task.start(product_id)
    except Exception as e:
        print(f'Exception scraping {product_id}: {e}')
