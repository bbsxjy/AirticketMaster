# -*- coding: utf-8 -*-

import scrapy
import time
from selenium import webdriver
from AirticketMaster import items
from AirticketMaster.utils.common_utils import *
from AirticketMaster.utils.email_alarm_utils import *

class DeltaAirlineHelper:

    travel_plan = {
        ("SEA", "PVG"):
            [
             '2020-06-29', '2020-06-30', '2020-07-01', '2020-07-02', '2020-07-03',
             '2020-07-06', '2020-07-07', '2020-07-08', '2020-07-09', '2020-07-10',
             '2020-07-13', '2020-07-14', '2020-07-15', '2020-07-16', '2020-07-17',
             ]
    }

    def __init__(self):
        self.email_helper = EmailAlarmUtility()

    def parse(self, url, driver):

        for planed_city in self.travel_plan.keys():
            try:
                planed_date = self.travel_plan[planed_city]
                driver.get(url)
                time.sleep(10)

                trip_button = driver.find_element_by_xpath("(//span[@aria-describedby='selectTripType-val'])")
                trip_button.click()

                time.sleep(2)

                one_way = driver.find_element_by_xpath("(//li[text()='One Way'])")
                one_way.click()

                time.sleep(2)

                departure_city_box = driver.find_element_by_xpath("//a[@id='fromAirportName']")
                departure_city_box.click()

                time.sleep(2)

                departure_city = driver.find_element_by_xpath("//input[@id='search_input']")
                departure_city.clear()
                departure_city.send_keys(planed_city[0])

                time.sleep(2)

                city_list = driver.find_elements_by_xpath("//li[@class='airport-list ng-star-inserted']")
                first_city = city_list[0].find_element_by_css_selector("a[tabindex='-1']")
                first_city.click()

                time.sleep(5)

                arrival_city_box = driver.find_element_by_xpath("//a[@id='toAirportName']")
                arrival_city_box.click()

                time.sleep(2)

                arrival_city = driver.find_element_by_xpath("//input[@id='search_input']")
                arrival_city.clear()
                arrival_city.send_keys(planed_city[-1])

                time.sleep(2)

                city_list = driver.find_elements_by_xpath("//li[@class='airport-list ng-star-inserted']")
                first_city = city_list[0].find_element_by_css_selector("a[tabindex='-1']")
                first_city.click()

                time.sleep(5)

                d_date_box = driver.find_element_by_css_selector("span[id='calDepartLabelCont']")
                d_date_box.click()

                time.sleep(10)

                d_date = driver.find_element_by_xpath("//a[@aria-label='%s']" % get_modified_date_format(planed_date[0], '%Y-%m-%d', '%d %B %Y, %A'))
                d_date.click()
                time.sleep(5)

                search_button = driver.find_element_by_id("btn-book-submit")
                search_button.click()
                time.sleep(20)

                self.wrap_up_search_results(driver, planed_date[0], planed_city)

                for date in planed_date[1:]:
                    try:
                        d_date_box = driver.find_element_by_css_selector("span[id='calDepartLabelCont']")
                        d_date_box.click()

                        time.sleep(2)

                        d_date = driver.find_element_by_xpath(
                            "//a[@aria-label='%s']" % get_modified_date_format(date, '%Y-%m-%d',
                                                                               '%d %B %Y, %A'))
                        d_date.click()
                        time.sleep(5)

                        search_button = driver.find_element_by_id("btnSubmit")
                        search_button.click()
                        time.sleep(20)

                        self.wrap_up_search_results(driver, date, planed_city)
                    except:
                        continue
            except:
                continue

    def wrap_up_search_results(self, driver, date, planed_city):
        route_detail = items.Route()
        flight_detail = items.Flight()
        if is_element_present(driver, "div[class='flightcardtable selectedcolumn1 ng-star-inserted']"):

            flight_routes = driver.find_elements_by_css_selector("div[class='col-12 flightcardContainer ng-star-inserted']")
            print("Found %s flight_routes of the request => %s" % (len(flight_routes), flight_routes))

            for flight in flight_routes:
                try:
                    flight_detail["flight_num"] = flight.find_element_by_css_selector(
                        "a[class='upsellpopupanchor ng-star-inserted']").text
                    route_detail["departure_city"] = planed_city[0]
                    route_detail["arrival_city"] = planed_city[-1]
                    route_detail["departure_time"] = flight.find_element_by_css_selector(
                        "div[class='totalTime']").text

                    classes = flight.find_elements_by_class_name('farecellitem')
                    for clazz in classes:
                        flight_detail["ticket_price"] = clazz.find_element_by_css_selector(
                            "a[class='farecellinkcontainer ng-star-inserted']").text
                        self.email_helper.trigger(route_detail, flight_detail, date)
                except:
                    continue

