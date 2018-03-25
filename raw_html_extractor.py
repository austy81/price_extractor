import requests
from lxml import html
import extraction_result_error


class HtmlExtractor():

    def __init__(self):
        pass

    def get_element_text(self, url, parser):
        try:
            r = requests.get(url)
            if r.status_code != 200:
                return "error url"
            tree = html.fromstring(r.content)
            price_element = tree.xpath(parser['price_element']+'/text()')
            return price_element[0], None
        except Exception as e:
            return 'error', extraction_result_error.ERROR_PARSING_PRICE

    def quit(self):
        pass
