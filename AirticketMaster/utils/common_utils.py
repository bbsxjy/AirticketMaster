# -*- coding: utf-8 -*-
__author__ = 'xjingyu'

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