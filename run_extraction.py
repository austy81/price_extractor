import re
import parser_matcher
import time
import multiprocessing 
import logging
import timer

from excel import excel
from html_extractor import HtmlExtractor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
    # ,filename="robot_extractor.log"
    )

def main():
    input_xlsx_file = "in.xlsx"
    output_xslx_file = "out.xlsx"
    insert_sheet_name = "results"
    url_column = 0
    url_sheet_name = "urls"
    parsers_sheet_name = "settings"

    logging.info("Loading input Excel...{}".format(input_xlsx_file))
    my_excel = excel(input_xlsx_file, output_xslx_file, insert_sheet_name)
    
    logging.info("Loading urls from sheet name '{}' column number {}...".format(url_sheet_name,url_column))
    urls = my_excel.get_column_values(sheet_name=url_sheet_name,url_column=url_column)
    logging.info("{} urls loaded.".format(len(urls)))

    logging.info("Loading settings from sheet name '{}'...".format(parsers_sheet_name))
    parser_matcher.parsers = my_excel.get_parsers(sheet_name=parsers_sheet_name)
    logging.info("{} parsers loaded.".format(len(parser_matcher.parsers)))

    logging.info("Matching urls with parsers...")
    matched_urls = parser_matcher.match_parsers(urls)
    unmatched_urls = [t["urls"] for t in matched_urls if t["parser"]["price_element"] is None]
    if len(unmatched_urls) == 1: unmatched_urls = unmatched_urls[0] 
    logging.info("{} urls found parser.".format(len(urls)-len(unmatched_urls)))
    logging.info("{} urls has no parser.".format(len(unmatched_urls)))

    logging.info("{} processor cores found.".format(multiprocessing.cpu_count()))
    logging.info("ROBOT is STARTING the EXTRACTION")
    logging.info("------------------------------------------")

    # Version without progress reporting
    pool = multiprocessing.Pool(multiprocessing.cpu_count()*2)
    result_set = pool.map(process_urls_for_parser, matched_urls)

    # pool = multiprocessing.Pool()
    # result_set = pool.map_async(process_urls_for_parser, matched_urls)
    # remaining_tasks = 0
    # while (True):
    #     if (result_set.ready()): 
    #         break
    #     if remaining_tasks != result_set._number_left:
    #         logging.info("Waiting for {} batches to complete...".format(result_set._number_left))
    #         remaining_tasks = result_set._number_left
    #     time.sleep(1)

    pool.close()
    pool.join()
    logging.info("Saving results to excel.")
    my_excel.save_in_excel(result_set)
    #my_excel.save_in_excel(result_set.get())
    logging.info("DONE")

def process_urls_for_parser(parser_urls):
    start_time = time.time()
    extractor = HtmlExtractor()
    #logging.info("STARTING {:4d} urls [{}]".format(len(parser_urls["urls"]), parser_urls["parser"]["url_regex"]))
    for url in parser_urls["urls"]:
        try:
            url["price"] = extractor.get_element_text(
                url=url["url"],
                parser = parser_urls["parser"])
        except Exception, e:
            logging.error("EXCEPT {}".format(str(e)))
    extractor.quit()
    elapsed_time = time.time() - start_time
    url_count = len(parser_urls["urls"])
    s_per_url = elapsed_time / url_count
    logging.info("FINISHED {:4d} urls in {:4d} seconds - {:6.2f} s/url [{}]".format(url_count, int(elapsed_time), s_per_url, parser_urls["parser"]["url_regex"]))
    return parser_urls

if __name__ == '__main__':
    main()
    #C:\Python27\python.exe run_extraction.py