# -*- coding: utf-8 -*-

import scrapy
import time
from selenium import webdriver
from AirticketMaster import items
from AirticketMaster.utils.common_utils import *
from AirticketMaster.utils.email_alarm_utils import *
from selenium.webdriver.common.keys import Keys

class ChinaSouthernAirlineHelper:

    travel_plan = {
        ("LAX", "CAN"):
            ['2020-06-07', '2020-06-14', '2020-06-21', '2020-06-28'],
        ("AMS", "CAN"):
            ['2020-06-05', '2020-06-12', '2020-06-19', '2020-06-26'],
        ("SEL", "SHE"):
            ['2020-06-07', '2020-06-14', '2020-06-21', '2020-06-28'],
        ("PAR", "CAN"):
            ['2020-06-09', '2020-06-16', '2020-06-23', '2020-06-30'],
        ("PAR", "TSN"):
            ['2020-06-03', '2020-06-10', '2020-06-17', '2020-06-24']
    }

    def __init__(self):
        self.email_helper = EmailAlarmUtility()

    def parse(self, url, driver):
        for planed_city in self.travel_plan.keys():
            try:
                departure_city, arrival_city = planed_city[0], planed_city[-1]
                planed_dates = self.travel_plan[planed_city]
                driver.get(url)
                time.sleep(10)

                default_site_button = driver.find_element_by_xpath("(//a[@id='defalt-site-btn'])")
                default_site_button.click()
                time.sleep(10)


                one_way_button = driver.find_element_by_xpath("(//a[text()='单程'])")
                one_way_button.click()
                time.sleep(0.5)


                departure = driver.find_element_by_xpath("(//input[@name='fDepCity'])")
                departure.clear()
                departure.send_keys(departure_city)
                time.sleep(2)
                departure.send_keys(Keys.ENTER)

                time.sleep(5)

                arrival = driver.find_element_by_xpath("(//input[@name='fArrCity'])")
                arrival.clear()
                arrival.send_keys(arrival_city)
                time.sleep(2)
                arrival.send_keys(Keys.ENTER)

                time.sleep(5)

                d_date = driver.find_element_by_xpath("(//input[@name='fDepDate'])")
                d_date.click()
                time.sleep(5)

                r_date = driver.find_element_by_xpath("(//li[@data-value='%s']//a)" % planed_dates[0])
                r_date.click()

                time.sleep(1)

                search_button = driver.find_element_by_xpath("(//a[@class='fr searchBtn searchFlight'])")
                search_button.click()

                time.sleep(60)

                self.search_on_ticket_price(driver, planed_dates[0])

                for date in planed_dates[1:]:
                    try:

                        d_date = driver.find_element_by_xpath("(//input[@name='single-formCalender'])")
                        d_date.click()
                        time.sleep(5)

                        r_date = driver.find_element_by_xpath("(//li[@data-value='%s']//a)" % date)
                        r_date.click()

                        time.sleep(1)

                        search_button = driver.find_element_by_id("search-submit")
                        search_button.click()

                        time.sleep(60)

                        self.search_on_ticket_price(driver, date)
                    except:
                        continue
            except:
                continue


    def search_on_ticket_price(self, driver, date):
        flight_list = driver.find_elements_by_class_name('zls-flight-cell')
        print("Found %s flight_list of the request => %s" % (len(flight_list), flight_list))

        route_detail = items.Route()
        flight_detail = items.Flight()

        for flight in flight_list:
            try:
                flight_classes = flight.find_elements_by_css_selector("div[class='fligthR'] > ul > li")
                for clazz in flight_classes:
                    try:
                        print clazz.get_attribute('innerHTML')
                        print is_element_present(clazz, "i")
                        if is_element_present(clazz, "i"):
                            flight_detail["flight_num"] = flight.find_element_by_css_selector(
                                "div[class='zls-flgno-info']").text
                            flight_detail["ticket_price"] = clazz.text
                            route_detail["departure_city"] = flight.find_element_by_css_selector(
                                "div[class='zls-flgtime zls-flgtime-r zls-flgtime-dep'] > div[class='zls-flplace']").text
                            route_detail["arrival_city"] = flight.find_element_by_css_selector(
                                "div[class='zls-flgtime zls-flgtime-arr'] > div[class='zls-flplace']").text
                            route_detail["departure_time"] = flight.find_element_by_css_selector(
                                "div[class='zls-flgtime zls-flgtime-r zls-flgtime-dep']").text
                            self.email_helper.trigger(route_detail, flight_detail, date)
                    except:
                        continue
            except:
                continue