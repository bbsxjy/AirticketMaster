# -*- coding: utf-8 -*-

import scrapy
import time
from selenium import webdriver
from AirticketMaster import items
from AirticketMaster.utils.common_utils import *
from AirticketMaster.utils.email_alarm_utils import *
from selenium.webdriver.common.keys import Keys

'''
This airline has bad cx and broken login system. Need to review and re-do the bypass verification step.
For now, I just simply reload main page everytime. 

'''
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

            departure_city, arrival_city = planed_city[0], planed_city[-1]
            planed_dates = self.travel_plan[planed_city]

            for date in planed_dates:
                try:

                    driver.quit()
                    driver = webdriver.Chrome()

                    driver.get(url)
                    time.sleep(10)

                    try:
                        default_site_button = driver.find_element_by_xpath("(//a[@id='defalt-site-btn'])")
                        default_site_button.click()
                        time.sleep(10)
                    except:
                        pass

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

                    r_date = driver.find_element_by_xpath("(//li[@data-value='%s']//a)" % date)
                    r_date.click()

                    time.sleep(1)

                    search_button = driver.find_element_by_xpath("(//a[@class='fr searchBtn searchFlight'])")
                    search_button.click()

                    time.sleep(60)

                    self.search_on_ticket_price(driver, date)

                except:
                    continue

    def search_on_ticket_price(self, driver, date):
        try:
            class_tab_list = driver.find_elements_by_css_selector(
                            "div[class='sh-cabin-tab'] > ul > li")
            print("Found %s class_tab_list of the request => %s" % (len(class_tab_list), class_tab_list))

            route_detail = items.Route()
            flight_detail = items.Flight()

            for clazz in class_tab_list:
                class_tab = clazz.find_element_by_css_selector("a")
                class_tab.click()
                time.sleep(5)

                flight_list = driver.find_elements_by_class_name('item')
                print("Found %s flight_list of the request => %s" % (len(flight_list), flight_list))

                for flight in flight_list:
                    try:
                        if is_element_present(flight, "a[class='cm-btn btn-red j-choose']"):
                            flight_detail["flight_num"] = flight.find_element_by_css_selector(
                                "div[class='caption']").text
                            flight_detail["ticket_price"] = flight.find_element_by_css_selector(
                                "strong[class='num sh-prc-fare'] > ").text

                            flight_info = flight.find_elements_by_css_selector(
                                "div[class='sh-intro'] > ul > li")

                            route_detail["departure_city"] = flight_info[0].text
                            route_detail["arrival_city"] = flight_info[2].text
                            route_detail["departure_time"] = flight_info[0].find_element_by_css_selector(
                                "strong[class='num']").text
                            self.email_helper.trigger(route_detail, flight_detail, date)
                    except:
                        continue
        except:
            pass