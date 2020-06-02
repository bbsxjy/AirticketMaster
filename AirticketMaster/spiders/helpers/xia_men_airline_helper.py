# -*- coding: utf-8 -*-

import time
from selenium.webdriver.common.keys import Keys
from AirticketMaster import items
from AirticketMaster.utils.common_utils import *
from AirticketMaster.utils.email_alarm_utils import *
from AirticketMaster.settings import *

class XiamenAirlineHelper:
    travel_plan = {
        ("luoshanji", "xiamen"):
            ['2020-06-08', '2020-06-15', '2020-06-22', '2020-06-29'],
        ("dongjing", "fuzhou"):
            ['2020-06-03', '2020-06-10', '2020-06-17', '2020-06-24'],
        ("amusitedan", "xiamen"):
            ['2020-06-03', '2020-06-10', '2020-06-17', '2020-06-24'],
        ("shouer", "xiamen"):
            ['2020-06-08', '2020-06-15', '2020-06-22', '2020-06-29'],
    }

    def __init__(self):
        self.email_helper = EmailAlarmUtility()

    def parse(self, url, driver):
        travel_option = items.TravelOption()

        for planed_city in self.travel_plan.keys():
            try:

                flights_list = []
                route_list = []
                departure_city = planed_city[0]
                arrival_city = planed_city[-1]
                planed_dates = self.travel_plan[planed_city]

                driver.get(url)
                time.sleep(10)

                alert_confirm_button = driver.find_element_by_xpath("//div[@class='cancelBox']//button")
                alert_confirm_button.click()

                time.sleep(5)

                one_way_button = driver.find_element_by_class_name("one-way")
                one_way_button.click()

                time.sleep(0.5)

                departure = driver.find_element_by_xpath("(//input[@placeholder='出发城市'])")
                departure.clear()
                departure.send_keys(departure_city)
                departure.send_keys(Keys.ENTER)

                time.sleep(5)

                arrival = driver.find_element_by_xpath("(//input[@placeholder='到达城市'])")
                arrival.clear()
                arrival.send_keys(arrival_city)
                arrival.send_keys(Keys.ENTER)

                time.sleep(5)

                # next_button = driver.find_element_by_xpath("(//span[@class='datepicker-nextBtn glyphicon glyphicon-chevron-right'])")
                # next_button.click()
                # time.sleep(1)
                # next_button.click()
                # time.sleep(1)

                arrival = driver.find_element_by_xpath("(//span[@data-date='{}'])".format(planed_dates[0]))
                arrival.click()

                time.sleep(1)

                search_button = driver.find_element_by_xpath("(//div[@class='btn-large-yellow'])")
                search_button.click()

                time.sleep(20)

                price_detail = self.is_price_table_showed(driver, "span[class='up']")

                if price_detail:

                    self.wrap_up_search_results(driver, flights_list, route_list, travel_option, planed_dates[0])

                else:

                    for date in planed_dates[1:]:
                        departure_date_input = driver.find_element_by_xpath("(//input[@placeholder='去程日期'])")
                        departure_date_input.clear()
                        departure_date_input.send_keys(date)

                        time.sleep(3)

                        search_button = driver.find_element_by_xpath("(//div[@class='right search J_Search'])")
                        search_button.click()

                        time.sleep(20)

                        price_detail = self.is_price_table_showed(driver, "div[class='up']")

                        if price_detail:
                            self.wrap_up_search_results(driver, flights_list, route_list, travel_option, date)

            except:

                continue

        return travel_option

    def is_price_table_showed(self, driver, field_name):
        price_detail = driver.find_elements_by_css_selector(field_name)
        print("Found %s price_detail of the request => %s" % (len(price_detail), price_detail))

        for d in price_detail:
            d.click()
            time.sleep(10)

        return price_detail


    def wrap_up_search_results(self, driver, flights_list, route_list, travel_option, date):
        all_routes = driver.find_elements_by_css_selector("div[class='list-group']")

        print("Found %s routes of the request" % len(all_routes))

        for route in all_routes:
            route_detail = items.Route()

            route_detail["departure_time"] = route.find_element_by_css_selector(
                "div[class='start'] > div[class='time']").text
            route_detail["departure_city"] = route.find_element_by_css_selector(
                "div[class='start'] > div[class='plane']").text
            route_detail["arrival_time"] = route.find_element_by_css_selector(
                "div[class='end'] > div[class='time']").text
            route_detail["arrival_city"] = route.find_element_by_css_selector(
                "div[class='end'] > div[class='plane']").text
            flight_num = route.find_element_by_css_selector("span[class='flight-num']").text
            flight_duration = route.find_element_by_css_selector("div[class='total-time']").text

            # xpath will find all elements, use css selector instead
            flightable_classes = route.find_elements_by_css_selector("div[class='item clearfix']")

            print("Found %s classes for flight %s to book" % (len(flightable_classes), flight_num))

            for fclass in flightable_classes:

                flight_detail = items.Flight()

                flight_detail["flight_num"] = flight_num
                flight_detail["flight_duration"] = flight_duration
                flight_detail["flight_class"] = fclass.find_element_by_css_selector("div[class='site']").text
                flight_detail["ticket_price"] = fclass.find_element_by_css_selector("div[class='price'] > strong").text
                flight_detail["remaining_ticket_status"] = fclass.find_element_by_css_selector(
                    "div[class='remark'] > span[class='orange']").text
                flight_detail["is_flight_bookable"] = is_element_present(fclass, "div[class='choose']")

                if flight_detail["is_flight_bookable"]:
                    self.email_helper.trigger(route_detail, flight_detail, date)

                flights_list.append(dict(flight_detail))

            route_detail["flight"] = empty_and_return_new_list(flights_list)

            route_list.append(dict(route_detail))

        travel_option['route_detail'] = empty_and_return_new_list(route_list)




