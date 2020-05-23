import scrapy
import time
from selenium import webdriver

class EasternAirlineSpider(scrapy.Spider):
    name = 'eastern_airline_spider'
    allowed_domains = ['ceair.com']
    start_urls = ['http://www.ceair.com/']

    def __init__(self):
        self.driver = webdriver.Chrome()

    def parse(self, response):
        print("get selenium driver")
        driver = self.driver
        driver.get(response.url)

        driver.maximize_window()

        time.sleep(5)


        driver.quit()