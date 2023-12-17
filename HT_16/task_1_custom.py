# Покрито катомним Exception
import csv
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from random import randrange
from typing import Tuple

import requests
from PIL import Image
from selenium import webdriver
from selenium.common import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from xhtml2pdf import pisa


@dataclass
class RobotOrderInputData:
    order_number: str
    head: str
    body: str
    legs: str
    address: str


@dataclass
class RobotOrderReceipt:
    id: str
    content: str


class RobotSpareBinException(Exception):
    pass


class RobotSpareBin:
    RESULT_DIR = Path(Path.cwd(), 'output')

    BASE_URL = 'https://robotsparebinindustries.com'
    ORDERS_URL = 'https://robotsparebinindustries.com/orders.csv'

    ACTION_TIMEOUT = 1
    WAIT_TIMEOUT = 10

    DEFAULT_SERVICE_ARGS = [
        '--allow-running-insecure',

        '--no-sandbox',
        '--hide-scrollbars',
        '--disable-infobars',

        '--disable-application-cache',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--disable-notifications',
        '--disable-setuid-sandbox',
        '--disable-web-security',
    ]

    def __init__(self):
        chrome_options = ChromeOptions()

        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option(
            'prefs', {
                'profile.default_content_setting_values.notifications': 2,
                'profile.default_content_settings.popups': 0,
            })
        for arg in self.DEFAULT_SERVICE_ARGS:
            chrome_options.add_argument(arg)

        self.__driver = webdriver.Chrome(service=ChromService(ChromeDriverManager().install()), options=chrome_options)
        self.__driver.maximize_window()

    def create_results_dir(self):
        try:
            if self.RESULT_DIR.is_dir():
                shutil.rmtree(self.RESULT_DIR)
            self.RESULT_DIR.mkdir(parents=True, exist_ok=True)
        except Exception:
            raise RobotSpareBinException('invalid results dir created')

    def remove_file(self, file):
        try:
            if file and os.path.exists(file):
                os.remove(file)
        except Exception:
            raise RobotSpareBinException(f'invalid remove file {file}')

    def get_orders_data(self):
        try:
            request = requests.get(self.ORDERS_URL)
            request.raise_for_status()
            rows = csv.reader(request.text.splitlines()[1:])
            return [RobotOrderInputData(*row) for row in rows]
        except requests.HTTPError:
            raise RobotSpareBinException('invalid request')
        except Exception:
            raise RobotSpareBinException('invalid get orders data')

    def wait_until(self, timeout: int = ACTION_TIMEOUT):
        action = webdriver.ActionChains(self.__driver)
        action.pause(randrange(timeout, timeout + 5, 1))
        action.perform()

    def wait_locator(self, locator: Tuple[str, str], is_click: bool = True):
        driver_wait = WebDriverWait(self.__driver, self.WAIT_TIMEOUT)
        element = driver_wait.until(EC.presence_of_element_located(locator))
        if is_click:
            element.click()

    def open_order_page(self):
        try:
            self.__driver.get(self.BASE_URL)
            self.wait_locator((By.LINK_TEXT, "Order your robot!"))
        except (WebDriverException, NoSuchElementException):
            raise RobotSpareBinException('invalid open order page')

    def do_order(self, order_data: RobotOrderInputData):
        try:
            self.wait_locator((By.CSS_SELECTOR, 'button.btn-dark'))
            print('order tab open')

            self.set_order_fields(order_data)
            print('order fields set')

            preview_img_file = Path(self.RESULT_DIR, f'tmp_{order_data.order_number}_robot.png')
            self.save_preview_image(preview_img_file)
            print('get preview imag')

            receipt = self.get_receipt()
            self.save_receipt_to_pdf(receipt, preview_img_file)
            print(f'new receipt {receipt.id} save done')
        except RobotSpareBinException as e:
            print(f'invalid create order with order data number {order_data.order_number}: {e}')

    def set_order_fields(self, order_data: RobotOrderInputData):
        try:
            header_input = self.__driver.find_element(By.NAME, 'head')
            body_input = self.__driver.find_element(By.ID, f'id-body-{order_data.body}')
            legs_input = self.__driver.find_element(By.XPATH, '//input[@class="form-control"][@type="number"]')
            address_input = self.__driver.find_element(By.XPATH, '//input[@class="form-control"][@type="text"]')

            header_input = Select(header_input)
            header_input.select_by_value(str(order_data.head))
            self.wait_until()

            legs_input.send_keys(order_data.legs)
            self.wait_until()

            address_input.send_keys(order_data.address)
            self.wait_until()

            body_input.click()
            self.wait_until()
        except (WebDriverException, NoSuchElementException):
            raise RobotSpareBinException('invalid set order fields')

    def open_preview_image(self):
        try:
            self.__driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.wait_locator((By.ID, 'preview'))
            self.wait_locator((By.ID, 'robot-preview-image'), False)
        except (TimeoutException, WebDriverException, NoSuchElementException):
            raise RobotSpareBinException('invalid get preview image')

    def save_preview_image(self, file: Path):
        self.open_preview_image()

        try:
            head_img_url = self.__driver.find_element(By.XPATH, '//img[@alt="Head"]').get_attribute('src')
            body_img_url = self.__driver.find_element(By.XPATH, '//img[@alt="Body"]').get_attribute('src')
            legs_img_url = self.__driver.find_element(By.XPATH, '//img[@alt="Legs"]').get_attribute('src')

            head_img = Image.open(requests.get(head_img_url, stream=True).raw)
            body_img = Image.open(requests.get(body_img_url, stream=True).raw)
            legs_img = Image.open(requests.get(legs_img_url, stream=True).raw)

            img_width = max(head_img.size[0], body_img.size[0], legs_img.size[0])
            img_height = head_img.size[1] + body_img.size[1] + legs_img.size[1]

            img = Image.new("RGBA", (img_width, img_height))
            img.paste(head_img, (int((img_width - head_img.size[0]) / 2), 0))
            img.paste(body_img, (int((img_width - body_img.size[0]) / 2), head_img.size[1]))
            img.paste(legs_img, (int((img_width - legs_img.size[0]) / 2), head_img.size[1] + body_img.size[1]))

            img.save(file)
        except (WebDriverException, NoSuchElementException):
            raise RobotSpareBinException('invalid parser html for save image')
        except Exception:
            raise RobotSpareBinException('invalid save preview image')

    def is_alert_danger(self) -> bool:
        try:
            self.__driver.find_element(By.CLASS_NAME, 'alert-danger')
            return True
        except (WebDriverException, NoSuchElementException):
            return False

    def is_order_successful(self) -> bool:
        try:
            self.wait_locator((By.ID, 'receipt'), False)
            return True
        except (WebDriverException, NoSuchElementException, TimeoutException):
            return not self.is_alert_danger()

    def get_receipt(self) -> RobotOrderReceipt:
        order_btn = self.__driver.find_element(By.ID, 'order')
        order_btn.click()

        while not self.is_order_successful():
            order_btn.click()

        try:
            _id = self.__driver.find_element(By.CLASS_NAME, 'badge-success').text
            _id = _id[_id.rfind('-') + 1:]

            receipt_element = self.__driver.find_element(By.ID, 'receipt')
            receipt_html = receipt_element.get_attribute('innerHTML')

            return RobotOrderReceipt(id=_id, content=receipt_html)
        except (WebDriverException, NoSuchElementException):
            raise RobotSpareBinException('invalid get order')

    def save_receipt_to_pdf(self, receipt: RobotOrderReceipt, preview_img_file: Path):
        try:
            content = f'{receipt.content}'

            if preview_img_file:
                content += f'<img src="{preview_img_file}"/>'

            file = Path(self.RESULT_DIR, f'{receipt.id}_robot.pdf')
            with open(file, "w+b") as pdf_file:
                pisa.CreatePDF(content, pdf_file)
                pdf_file.close()
        except Exception:
            raise RobotSpareBinException('invalid save pdf')
        else:
            self.remove_file(preview_img_file)

    def start(self):
        try:
            self.create_results_dir()
            orders_data = self.get_orders_data()
            print('get orders input data done')
            self.wait_until()

            self.open_order_page()
            for order_data in orders_data:
                self.do_order(order_data)
                self.wait_locator((By.ID, 'order-another'))

        except RobotSpareBinException as e:
            print(f'Exception: {e}')
        else:
            print('Done')
        finally:
            self.__driver.close()
            self.__driver.quit()


robot = RobotSpareBin()
robot.start()
