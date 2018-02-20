from excel import excel
from html_extractor import HtmlExtractor
import re
import parser_matcher
import time
from multiprocessing import Pool

def main():
    input_xlsx_file = "in.xlsx"
    output_xslx_file = "out.xlsx"
    insert_sheet_name = "results"
    my_excel = excel(input_xlsx_file, output_xslx_file, insert_sheet_name)
    urls = my_excel.get_column_values(sheet_name="urls",url_column=3)
    parser_matcher.parsers = my_excel.get_parsers(sheet_name="parsers")
    matched_urls = parser_matcher.match_parsers(urls)

    pool = Pool(8)
    prices = pool.map(process_urls_for_parser, matched_urls)
    #prices = [process_urls_for_parser(matched_urls[0])]
    my_excel.save_in_excel(prices)

def process_urls_for_parser(parser_urls):
    extractor = HtmlExtractor()
    for url in parser_urls["urls"]:
        try:
            url["price"] = extractor.get_element_text(
                url=url["url"],
                parser = parser_urls["parser"])
        except Exception, e:
            print("EXCEPT {}".format(str(e)))
        print("[{}] {}".format(url["price"],url["url"]))
    extractor.quit()
    return parser_urls

if __name__ == '__main__':
    main()