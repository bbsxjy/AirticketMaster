# -*- coding: utf-8 -*-
__author__ = 'xjingyu'

import datetime

def is_element_present(driver, ele_xpath):
    try:
        if driver.find_element_by_css_selector(ele_xpath):
            return True
        return False
    except:
        return False

def empty_and_return_new_list(old):
    new = []
    length = len(old)
    for i in range(length):
        new.append(old.pop(-1))
    new.reverse()
    return new

def get_modified_date_format(input_date_str, input_date_format, output_date_format):
    date = datetime.datetime.strptime(input_date_str, input_date_format).date()
    return date.strftime(output_date_format)
