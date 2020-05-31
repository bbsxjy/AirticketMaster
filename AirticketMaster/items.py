# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class TravelOption(scrapy.Item):
    route_detail = scrapy.Field()

class Route(scrapy.Item):
    transfer = scrapy.Field()
    num_of_transfer = scrapy.Field()
    flight = scrapy.Field()
    departure_time = scrapy.Field()
    departure_city = scrapy.Field()
    arrival_time = scrapy.Field()
    arrival_city = scrapy.Field()

class Flight(scrapy.Item):
    flight_num = scrapy.Field()
    remaining_ticket_status = scrapy.Field()
    flight_duration = scrapy.Field()
    is_flight_bookable = scrapy.Field()
    ticket_price = scrapy.Field()
    flight_class = scrapy.Field()
