from selenium import webdriver
import re
# from time import strftime


class HtmlExtractor():

    def __init__(self):
        # from selenium.webdriver.chrome.options import Options
        # from selenium.webdriver.remote.remote_connection import LOGGER
        # import logging
        # LOGGER.setLevel(logging.ERROR)
        # chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # self.driver = webdriver.Chrome(chrome_options=chrome_options)
        # self.driver.set_window_size(1120, 550)
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 550)

    def get_element_text(self, url, parser):
        price_element = parser['price_element']
        if price_element is None:
            return "n/a"  # No parser
        verify_exists = parser['verify_exists']
        verify_not_exists = parser['verify_not_exists']

        try:
            return_val = None,  # 'error opening url'
            self.driver.get(url)

            if verify_exists is not None:
                try:
                    self.driver.find_element_by_xpath(verify_exists)
                except Exception:
                    return None  # element which should exsist was not found

            if verify_not_exists is not None:
                try:
                    self.driver.find_element_by_xpath(verify_not_exists)
                    return None  # found element which should not exist
                except Exception:
                    pass

            return_val = None  # 'error finding price on page'
            element_text = self.driver.find_element_by_xpath(
                price_element).text.encode('ascii', errors='ignore')
            return_val = None  # "'{}' error parsing price".format(element_text)
            return self._get_price(element_text)
        except Exception:
            # self.driver.save_screenshot('screenshots/screenshot_{}.png'.format(strftime("%Y_%m_%d_%H_%M_%S")))
            return return_val

    def _get_price(self, text):
        text = text.decode('utf-8')
        nums = re.findall(r"\d+", text.replace(" ", ""))
        if len(nums) == 0:
            return None  # "price element does not contain numbers"
        if len(nums) == 1:
            return int(nums[0])
        if len(nums) == 2:
            return float("{}.{}".format(nums[0], nums[1]))
        return None  # "too many numeric values in price element"

    def quit(self):
        self.driver.quit()
