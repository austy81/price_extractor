from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import strftime
import re
import logging


class HtmlExtractor():

    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 550)

    def get_element_text(self, url, parser):
        price_element=parser['price_element']
        if price_element is None:
            return "No parser"
        verify_exists=parser['verify_exists']
        verify_not_exists=parser['verify_not_exists']

        try:
            return_val = 'error opening url'
            self.driver.get(url)

            if verify_exists is not None:
                try:
                    self.driver.find_element_by_xpath(verify_exists)
                except:
                    return 'n/a'

            if verify_not_exists is not None:
                try:
                    self.driver.find_element_by_xpath(verify_not_exists)
                    return 'n/a'
                except:
                    pass

            return_val = 'error finding price on page'
            element_text = self.driver.find_element_by_xpath(price_element).text.encode('ascii', errors='ignore')
            return_val = "'{}' error parsing price".format(element_text)
            return self._get_price(element_text)
        except Exception, e:
            #self.driver.save_screenshot('screenshots/screenshot_{}.png'.format(strftime("%Y_%m_%d_%H_%M_%S")))
            return "{} Exception:{}".format(return_val, repr(e))

    def _get_price(self, text):
        nums = re.findall(r"\d+", text.replace(" ",""))
        if len(nums)==0:
            return "price element does not contain numbers"
        if len(nums)==1:
            return int(nums[0])
        if len(nums)==2:
            return float("{}.{}".format(nums[0],nums[1]))
        return "too many numeric values in price element"

    def quit(self):
        self.driver.quit()

