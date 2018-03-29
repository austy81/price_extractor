import requests
from lxml import html
import extraction_result_error
import extract_price


class HtmlExtractor():

    def __init__(self):
        pass

    def get_element_text(self, url, parser):
        try:
            r = requests.get(url)
            if r.status_code != 200:
                return None, extraction_result_error.ERROR_OPENING_URL

            tree = html.fromstring(r.content)

            if parser['verify_exists'] and len(tree.xpath(parser['verify_exists'])) < 1:
                return None, extraction_result_error.ELEMENT_SHOULD_EXIST

            if parser['verify_not_exists'] and len(tree.xpath(parser['verify_not_exists'])) > 0:
                return None, extraction_result_error.ELEMENT_SHOULD_NOT_EXIST

            price_element = tree.xpath(parser['price_element']+'/text()')
            return extract_price.clean(price_element[0] if len(price_element) > 0 else None), None
        except Exception as e:
            return None, extraction_result_error.ERROR_PARSING_PAGE

    def quit(self):
        pass
