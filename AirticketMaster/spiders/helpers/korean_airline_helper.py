# -*- coding: utf-8 -*-

import scrapy
import time
from selenium import webdriver

class KoreanAirlineHelper:

    def parse(self, url, driver):
        print("get selenium driver")
        driver.get(url)

        time.sleep(10)

        one_way_button = driver.find_element_by_xpath("(//label[@for='oneway'])")
        one_way_button.click()

        departure_city = driver.find_element_by_xpath("(//input[starts-with(@id, 'KE') and contains(@id, '-28')])")
        departure_city.clear()
        departure_city.send_keys("ICN")

        time.sleep(1)

        arrival_city = driver.find_element_by_xpath("(//input[starts-with(@id, 'KE') and contains(@id, '-29')])")
        arrival_city.clear()
        arrival_city.send_keys("shenyang")

        time.sleep(1)

        d_date = driver.find_element_by_xpath("(//input[starts-with(@id, 'KE') and contains(@id, '-30')])")
        d_date.clear()
        d_date.send_keys("2020-06-05")

        time.sleep(1)

        search_button = driver.find_element_by_id("submit")
        search_button.click()

        time.sleep(15)
