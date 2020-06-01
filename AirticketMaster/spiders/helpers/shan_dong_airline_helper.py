# -*- coding: utf-8 -*-

import time
from selenium.webdriver.common.keys import Keys
from AirticketMaster import items
from AirticketMaster.utils.common_utils import *
from AirticketMaster.utils.email_alarm_utils import *
from AirticketMaster.settings import *

class ShandongAirlineHelper:

    def __init__(self):
        self.email_helper = EmailAlarmUtility()

    def parse(self, url, driver):
        travel_option = items.TravelOption()






