# -*- coding: utf-8 -*-

import scrapy
import time
from selenium import webdriver

class ChinaSouthernAirlineHelper:

    def parse(self, url, driver):
        driver.get(url)
        time.sleep(10)

