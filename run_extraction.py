import parser_matcher
import time
import multiprocessing
import logging
import os.path
import datetime
from excel import excel
from html_extractor import HtmlExtractor
# from raw_html_extractor import HtmlExtractor


def main():
    input_xlsx_file = r"excel\in.xlsx"
    output_xslx_file = r"excel\out.xlsx"
    insert_sheet_name = "results"
    url_column = 0
    url_sheet_name = "urls"
    parsers_sheet_name = "settings"

    setup_logging()
    logging.info("Loading input Excel...{}".format(input_xlsx_file))
    my_excel = excel(input_xlsx_file, output_xslx_file, insert_sheet_name)

    logging.info("Loading urls from sheet name '{}' column number {}...".format(
        url_sheet_name, url_column))
    urls = my_excel.get_column_values(
        sheet_name=url_sheet_name, url_column=url_column)
    logging.info("{} urls loaded.".format(len(urls)))

    logging.info("Loading settings from sheet name '{}'...".format(
        parsers_sheet_name))
    parser_matcher.parsers = my_excel.get_parsers(
        sheet_name=parsers_sheet_name)
    logging.info("{} parsers loaded.".format(len(parser_matcher.parsers)))

    logging.info("Matching urls with parsers...")
    matched_urls = parser_matcher.match_parsers(urls)
    unmatched_urls = [t["urls"]
                      for t in matched_urls if t["parser"]["price_element"] is None]
    if len(unmatched_urls) == 1:
        unmatched_urls = unmatched_urls[0]
    logging.info("{} urls found parser.".format(
        len(urls) - len(unmatched_urls)))
    logging.info("{} urls has no parser.".format(len(unmatched_urls)))

    logging.info("{} processor cores found.".format(
        multiprocessing.cpu_count()))
    logging.info("ROBOT is STARTING the EXTRACTION")
    logging.info("------------------------------------------")

    # Version without progress reporting
    pool = multiprocessing.Pool()
    result_set = pool.map(process_urls_for_parser, matched_urls)
    logging.info("Saving results to excel.")
    my_excel.save_in_excel(result_set)

    # single thread
    # result_set = map(process_urls_for_parser, matched_urls)
    # result_set = []
    # for urls in matched_urls:
    #     result_set.append(process_urls_for_parser(urls))
    # logging.info("Saving results to excel.")
    # my_excel.save_in_excel(result_set)

    # pool = multiprocessing.Pool()
    # result_set = pool.map_async(process_urls_for_parser, matched_urls)
    # pool.close()
    # remaining_tasks = 0
    # while (True):
    #     if (result_set.ready()):
    #         break
    #     if remaining_tasks != result_set._number_left:
    #         logging.info("Waiting for {} batches to complete...".format(result_set._number_left))
    #         remaining_tasks = result_set._number_left
    #     time.sleep(1)
    # logging.info("Saving results to excel.")
    # my_excel.save_in_excel(result_set.get())

    logging.info("DONE")


def process_urls_for_parser(parser_urls):
    extractor = HtmlExtractor()
    start_time = time.time()
    # logging.info("STARTING {:4d} urls [{}]".format(len(parser_urls["urls"]), parser_urls["parser"]["url_regex"]))
    for url in parser_urls["urls"]:
        try:
            url["price"] = extractor.get_element_text(
                url=url["url"],
                parser=parser_urls["parser"])
        except Exception as e:
            logging.error("EXCEPT {}".format(repr(e)))
            url["price"] = repr(e)
    elapsed_time = time.time() - start_time
    extractor.quit()
    url_count = len(parser_urls["urls"])
    s_per_url = elapsed_time / url_count
    print("{} FINISHED {:4d} urls in {:4d} seconds - {:6.2f} s/url [{}]".format(
        datetime.datetime.now().isoformat(), url_count, int(elapsed_time), s_per_url, parser_urls["parser"]["url_regex"]))
    return parser_urls


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # create console handler and set level to debug
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    # create file handler
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    file_handler = logging.FileHandler(r'logs/price_robot.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
