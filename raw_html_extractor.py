import requests


class HtmlExtractor():

    def __init__(self):
        pass

    def get_element_text(self, url, parser):
        try:
            r = requests.get(url)
            if r.status_code != 200:
                return "error url"
            return r.text
        except Exception as e:
            return repr(e)

    def quit(self):
        pass
