# -*- coding: utf-8 -*-

import scrapy
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from AirticketMaster import items
from AirticketMaster.utils.common_utils import *
from AirticketMaster.utils.email_alarm_utils import *
from AirticketMaster.settings import *

class ChinaEasternAirlineHelper:

    travel_plan = {
        ("ICN", "PVG"):
            ['2020-06-05', '2020-06-12', '2020-06-19', '2020-06-26'],
        ("NYC", "PVG"):
            ['2020-06-03', '2020-06-10', '2020-06-17', '2020-06-24'],
        ("AMS", "PVG"):
            ['2020-06-08', '2020-06-15', '2020-06-22', '2020-06-29'],
        ("PAR", "PVG"):
            ['2020-06-07', '2020-06-14', '2020-06-21', '2020-06-28'],
        ("FRA", "PVG"):
            ['2020-06-09', '2020-06-16', '2020-06-23', '2020-06-30'],
        ("TYO", "PVG"):
            ['2020-06-05', '2020-06-12', '2020-06-19', '2020-06-26']
    }

    def __init__(self):
        self.email_helper = EmailAlarmUtility()


    def parse(self, url, driver):
        for planed_city in self.travel_plan.keys():

            try:
                departure_city, arrival_city = planed_city[0], planed_city[-1]
                driver.get(url)
                time.sleep(10)

                header = driver.find_element_by_id("header2018")

                one_way_button = driver.find_element_by_id("ga_cn_jpdc")
                one_way_button.click()

                time.sleep(0.5)

                header.click()

                departure = driver.find_element_by_xpath("(//input[@id='label_ID_0'])")
                departure.clear()
                departure.send_keys(departure_city)

                time.sleep(5)

                header.click()

                arrival = driver.find_element_by_xpath("(//input[@id='label_ID_1'])")
                arrival.clear()
                arrival.send_keys(arrival_city)

                time.sleep(5)
                header.click()

                for date in self.travel_plan[planed_city]:
                    try:
                        d_date = driver.find_element_by_xpath("(//input[@name='deptDt'])")
                        d_date.click()
                        time.sleep(5)

                        r_date = driver.find_element_by_xpath("(//div[@date='%s'])" % date)
                        r_date.click()

                        time.sleep(1)

                        search_button = driver.find_element_by_id("btn_flight_search")
                        search_button.click()

                        time.sleep(60)

                        driver.switch_to.window(driver.window_handles[-1])

                        flight_list = driver.find_elements_by_class_name('flight')
                        print("Found %s flight_list of the request => %s" % (len(flight_list), flight_list))

                        route_detail = items.Route()
                        flight_detail = items.Flight()

                        for flight in flight_list:
                            try:
                                if is_element_present(flight, "section[class='detail'] > dl > dd[name='lowest'] > sub"):
                                    flight_detail["flight_num"] = flight.find_element_by_css_selector("div[class='title']").text
                                    flight_detail["ticket_price"] = flight.find_element_by_css_selector(
                                        "section[class='detail'] > dl > dd[name='lowest']").text
                                    route_detail["departure_city"] = flight.find_element_by_css_selector(
                                        "div[class='airport r']").text
                                    route_detail["arrival_city"] = flight.find_element_by_css_selector(
                                        "div[class='airport']").text
                                    route_detail["departure_time"] = flight.find_element_by_css_selector(
                                        "div[class='airport r'] > time").text
                                    self.email_helper.trigger(route_detail, flight_detail, date)
                            except:
                                continue
                    except:
                        continue
            except:
                continue




