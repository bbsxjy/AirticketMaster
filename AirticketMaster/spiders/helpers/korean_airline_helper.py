# -*- coding: utf-8 -*-

import scrapy
import time
from selenium import webdriver
from AirticketMaster import items
from AirticketMaster.utils.common_utils import *
from AirticketMaster.utils.email_alarm_utils import *

class KoreanAirlineHelper:

    travel_plan = {
        ("ICN", "shenyang"):
            ['2020-06-05', '2020-06-12', '2020-06-19', '2020-06-26']
    }

    def __init__(self):
        self.email_helper = EmailAlarmUtility()

    def parse(self, url, driver):

        for planed_city in self.travel_plan.keys():
            try:

                planed_date = self.travel_plan[planed_city]

                driver.get(url)

                time.sleep(10)

                one_way_button = driver.find_element_by_xpath("(//label[@for='oneway'])")
                one_way_button.click()

                departure_city = driver.find_element_by_xpath("(//input[starts-with(@id, 'KE') and contains(@id, '-28')])")
                departure_city.clear()
                departure_city.send_keys(planed_city[0])

                time.sleep(5)

                arrival_city = driver.find_element_by_xpath("(//input[starts-with(@id, 'KE') and contains(@id, '-29')])")
                arrival_city.clear()
                arrival_city.send_keys(planed_city[-1])

                time.sleep(5)

                d_date = driver.find_element_by_xpath("(//input[starts-with(@id, 'KE') and contains(@id, '-30')])")
                d_date.clear()
                d_date.send_keys(planed_date[0])
                time.sleep(5)

                search_button = driver.find_element_by_id("submit")
                search_button.click()
                time.sleep(5)

                warning_button = driver.find_element_by_xpath("(//a[@id='btnModalPopupYes'])")
                warning_button.click()
                time.sleep(30)

                self.wrap_up_search_results(driver, planed_date[0])

                for date in planed_date[1:]:
                    try:
                        warning_button = driver.find_element_by_xpath("(//a[@id='btnModalPopupYes'])")
                        warning_button.click()
                        time.sleep(15)

                        d_date = driver.find_element_by_xpath("(//input[@class='tripdetail-input'])")
                        d_date.clear()
                        d_date.send_keys(date)
                        time.sleep(5)

                        submit_button = driver.find_element_by_xpath("(//button[@id='submit'])")
                        try:
                            submit_button.click()
                            submit_button.click()
                        except:
                            pass
                        time.sleep(10)

                        warning_button = driver.find_element_by_xpath("(//a[@id='btnModalPopupYes'])")
                        warning_button.click()
                        time.sleep(30)

                        self.wrap_up_search_results(driver, date)
                    except:
                        continue
            except:
                continue

    def wrap_up_search_results(self, driver, date):
        route_detail = items.Route()
        flight_detail = items.Flight()
        if is_element_present(driver, "div[id='new-summary-international-flexdate']"):
            continue_button = driver.find_element_by_css_selector("button[class='btn-fixed-mainst continue-button']")
            try:
                continue_button.click()
                continue_button.click()
            except:
                pass
            time.sleep(30)

            flight_routes = driver.find_elements_by_class_name("flightItem")
            print("Found %s flight_routes of the request => %s" % (len(flight_routes), flight_routes))

            for flight in flight_routes:
                if is_element_present(flight, "div[class='flight-fare-passenger-type'] > strong"):
                    try:
                        flight_detail["flight_num"] = flight.find_element_by_css_selector(
                            "span[data-title='Flight Number']").text
                        flight_detail["ticket_price"] = flight.find_element_by_css_selector(
                            "strong[data-title='Fare per adult']").text
                        route_detail["departure_city"] = flight.find_element_by_css_selector(
                            "span[data-title='Departure']").text
                        route_detail["arrival_city"] = flight.find_element_by_css_selector(
                            "span[data-title='Arrival']").text
                        route_detail["departure_time"] = flight.find_element_by_css_selector(
                            "span[class='flight-time']").text
                        self.email_helper.trigger(route_detail, flight_detail, date)
                    except:
                        continue
