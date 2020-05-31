# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver
from AirticketMaster import settings
from AirticketMaster.spiders.helpers \
    import china_eastern_airline_helper, korean_airline_helper, xia_men_airline_helper

'''

This spider is used to scraping given airline information and try the best to get the latest air ticket information
during the special time of COVID-19.

Ideally, we want to use parrallel call to make the maximum efficients. However, due to Selenium is not thread safe, this
version now is only sequencial call.

'''
class AggregatedAirlineSpider(scrapy.Spider):
    name = settings.SPIDER_NAME
    allowed_domains = settings.ALLOWED_DOMAINS
    start_urls = [
        settings.XIAMEN_AIRLINE_BASE_URL
    ]

    airline_dict = {
        settings.KOREAN_AIRLINE_BASE_URL: korean_airline_helper.KoreanAirlineHelper(),
        settings.CHINA_EASTERN_BASE_URL: china_eastern_airline_helper.ChinaEasternAirlineHelper(),
        settings.XIAMEN_AIRLINE_BASE_URL: xia_men_airline_helper.XiamenAirlineHelper()
    }

    def __init__(self):
        self.driver = webdriver.Chrome()

    def parse(self, response):
        # self.driver.maximize_window()
        while True:
            yield self.call_targeted_airline(response.url)
            time.sleep(600)

    def call_targeted_airline(self, url):
        return self.airline_dict[url].parse(url, self.driver)


