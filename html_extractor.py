from selenium import webdriver
import extraction_result_error
import extract_price


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
            return None, extraction_result_error.NO_PARSER
        verify_exists = parser['verify_exists']
        verify_not_exists = parser['verify_not_exists']

        try:
            return_val = None, extraction_result_error.ERROR_OPENING_URL
            self.driver.get(url)

            if verify_exists:
                try:
                    self.driver.find_element_by_xpath(verify_exists)
                except Exception:
                    return None, extraction_result_error.ELEMENT_SHOULD_EXIST

            if verify_not_exists:
                try:
                    self.driver.find_element_by_xpath(verify_not_exists)
                    return None, extraction_result_error.ELEMENT_SHOULD_NOT_EXIST
                except Exception:
                    pass

            return_val = None, extraction_result_error.ERROR_FINDING_PRICE
            element_text = self.driver.find_element_by_xpath(
                price_element).text.encode('ascii', errors='ignore')
            return_val = None, extraction_result_error.ERROR_PARSING_PRICE
            return extract_price.clean(element_text), None
        except Exception:
            # self.driver.save_screenshot('screenshots/screenshot_{}.png'.format(strftime("%Y_%m_%d_%H_%M_%S")))
            return return_val

    def quit(self):
        self.driver.quit()
