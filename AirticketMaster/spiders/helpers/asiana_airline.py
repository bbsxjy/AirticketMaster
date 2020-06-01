# -*- coding: utf-8 -*-

import scrapy
import time
from selenium import webdriver

class AsianaAirlineHelper:

    def parse(self, url, driver):
        print("get selenium driver")
        driver.get(url)

