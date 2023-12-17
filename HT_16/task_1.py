# Автоматизувати процес замовлення робота за допомогою Selenium
# 1. Отримайте та прочитайте дані з "https://robotsparebinindustries.com/orders.csv". Увага! Файл має бути прочитаний
#    з сервера кожного разу при запускі скрипта, не зберігайте файл локально.
# 2. Зайдіть на сайт "https://robotsparebinindustries.com/"
# 3. Перейдіть у вкладку "Order your robot"
# 4. Для кожного замовлення з файлу реалізуйте наступне:
#     - закрийте pop-up, якщо він з'явився. Підказка: не кожна кнопка його закриває.
#     - оберіть/заповніть відповідні поля для замовлення
#     - натисніть кнопку Preview та збережіть зображення отриманого робота. Увага! Зберігати треба тільки зображення
#       робота, а не всієї сторінки сайту.
#     - натисніть кнопку Order та збережіть номер чеку. Увага! Інколи сервер тупить і видає помилку, але повторне
#       натискання кнопки частіше всього вирішує проблему. Дослідіть цей кейс.
#     - переіменуйте отримане зображення у формат <номер чеку>_robot (напр. 123456_robot.jpg). Покладіть зображення
#       в директорію output (яка має створюватися/очищатися під час запуску скрипта).
#     - замовте наступного робота (шляхом натискання відповідної кнопки)
#
# ** Додаткове завдання (необов'язково)
#     - окрім збереження номеру чеку отримайте також HTML-код всього чеку
#     - збережіть отриманий код в PDF файл
#     - додайте до цього файлу отримане зображення робота (бажано на одній сторінці, але не принципово)
#     - збережіть отриманий PDF файл у форматі <номер чеку>_robot в директорію output. Окремо зображення робота
#       зберігати не потрібно. Тобто замість зображень у вас будуть pdf файли які містять зображення з чеком.
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
        if self.RESULT_DIR.is_dir():
            shutil.rmtree(self.RESULT_DIR)
        self.RESULT_DIR.mkdir(parents=True, exist_ok=True)

    def get_orders_data(self):
        request = requests.get(self.ORDERS_URL)
        request.raise_for_status()
        rows = csv.reader(request.text.splitlines()[1:])
        return [RobotOrderInputData(*row) for row in rows]

    def wait_until(self, timeout: int = ACTION_TIMEOUT):
        action = webdriver.ActionChains(self.__driver)
        action.pause(randrange(timeout, timeout + 2, 1))
        action.perform()

    def wait_locator(self, locator: Tuple[str, str], is_click: bool = True):
        driver_wait = WebDriverWait(self.__driver, self.WAIT_TIMEOUT)
        element = driver_wait.until(EC.presence_of_element_located(locator))
        if is_click:
            element.click()

    def open_order_page(self):
        self.__driver.get(self.BASE_URL)
        self.wait_locator((By.LINK_TEXT, "Order your robot!"))

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
        except (TypeError, TimeoutException, WebDriverException, NoSuchElementException):
            print(f'invalid create order with order data number: {order_data.order_number}')

    def set_order_fields(self, order_data: RobotOrderInputData):
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

    def open_preview_image(self):
        self.__driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.wait_locator((By.ID, 'preview'))
        self.wait_locator((By.ID, 'robot-preview-image'), False)

    def save_preview_image(self, file: Path):
        self.open_preview_image()

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

        _id = self.__driver.find_element(By.CLASS_NAME, 'badge-success').text
        _id = _id[_id.rfind('-') + 1:]

        receipt_element = self.__driver.find_element(By.ID, 'receipt')
        receipt_html = receipt_element.get_attribute('innerHTML')

        return RobotOrderReceipt(id=_id, content=receipt_html)

    def save_receipt_to_pdf(self, receipt: RobotOrderReceipt, preview_img_file: Path):
        content = f'{receipt.content}'

        if os.path.exists(preview_img_file):
            content += f'<img src="{preview_img_file}"/>'

        file = Path(self.RESULT_DIR, f'{receipt.id}_robot.pdf')
        with open(file, "w+b") as pdf_file:
            pisa.CreatePDF(content, pdf_file)
            pdf_file.close()

        if os.path.exists(preview_img_file):
            os.remove(preview_img_file)

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
        except Exception as e:
            print(f'Exception: {e}')
        else:
            print('Done')
        finally:
            self.__driver.close()
            self.__driver.quit()


robot = RobotSpareBin()
robot.start()
