import re

parsers = []

def match_parsers(urls):
    matched_parsers = {}
    for url in urls:
        parser = _get_parser(url["url"])
        if parser["url_regex"] in matched_parsers:
            matched_parsers[parser["url_regex"]]["urls"].append(url)
        else:
            matched_parsers[parser["url_regex"]] = {"parser":parser, "urls":[url]}
    return _get_values_list(matched_parsers)

def _get_parser(url):
    for parser in parsers:
        match = re.search(parser["url_regex"], url)
        if match:
            return parser
    return {"url_regex": None, "price_element":None, "verify_exists":None, "verify_not_exists":None}

def _get_values_list(dict):
    dictlist = []
    for key, value in dict.iteritems():
        dictlist.append(value)
    return dictlist