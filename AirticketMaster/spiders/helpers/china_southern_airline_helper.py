# -*- coding: utf-8 -*-

import scrapy
import time
from selenium import webdriver

class ChinaSouthernAirlineHelper:

    def parse(self, url, driver):
        driver.get(url)
        time.sleep(10)

        header = driver.find_element_by_id("header2018")

        one_way_button = driver.find_element_by_id("ga_cn_jpdc")
        one_way_button.click()

        time.sleep(0.5)

        header.click()

        departure = driver.find_element_by_xpath("(//input[@id='label_ID_0'])")
        departure.clear()
        departure.send_keys("ICN")

        time.sleep(5)

        header.click()

        arrival = driver.find_element_by_xpath("(//input[@id='label_ID_1'])")
        arrival.clear()
        arrival.send_keys("PVG")

        time.sleep(5)
        header.click()

        d_date = driver.find_element_by_xpath("(//label[@for='depDt'])")
        d_date.click()
        time.sleep(0.5)
        r_date = driver.find_element_by_xpath("(//div[@date='2020-06-05'])")
        r_date.click()

        time.sleep(1)

        search_button = driver.find_element_by_id("btn_flight_search")
        search_button.click()

        time.sleep(10)

