import scrapy
from scrapy_splash import SplashRequest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from uniqlo.items import UniqloItem


class ProductsSpider(scrapy.Spider):
    basedir = os.path.dirname(os.path.realpath('__file__'))
    chrome_driver_path = os.path.join(basedir, 'chromedriver')
    LOGGER.setLevel(logging.WARNING)

    name = 'products'
    allowed_domains = ['uniqlo.com']
    start_urls = ['https://www.uniqlo.com/sg/en']

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options, executable_path=self.chrome_driver_path)

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 2})

    def parse(self, response):
        # links to men, women, child, kids
        # links = response.css('a[class="fr-global-nav-item px-s"]').css('a::attr(href)').getall()
        count=0
        for url, text in self.get_category_links_selenium(response.url):
            yield SplashRequest(url, self.parse_category_link, meta={'url': url, 'text': text, 'nav': 'women'}, args={'wait': 5})
            count+=1
            print('\n\n', count, '\n\n')
            print('\n\n', text, '\n\n')

    def get_category_links_selenium(self, url):
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 3)
        navs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".fr-global-nav-item")))
        nav_women = navs[0]

        print('\n\n' + nav_women.text + '\n\n')
        nav = nav_women

        ActionChains(self.driver).move_to_element(nav).perform()
        categories = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".w12-f [href]")))
        categories_urls = [elem.get_attribute('href') for elem in categories]
        categories_text = [elem.get_attribute('text') for elem in categories]
        return zip(categories_urls, categories_text)

    def parse_category_link(self, response):
        item_links = response.css(".fr-grid-item").css('.w4').css('a::attr(href)').getall()
        if item_links:
            for item_link in item_links:
                url = response.urljoin(item_link)
                yield SplashRequest(url, self.parse_item, args={'wait': 5})

    def parse_item(self, response):
        item = UniqloItem()
        name = response.xpath('//span[has-class("title", "fr-no-uppercase")]/text()').get()
        price = response.css('div[data-test="product-detail-summary"]').css('div.price').css('span::text').get()
        description = response.css('div[data-test="product-detail-summary"]').css('div.fr-text::text').get()

        item['name'] = name
        item['price'] = price
        item['description'] = description

        print('\n\n')
        print(item)
        print('\n\n')

        yield item