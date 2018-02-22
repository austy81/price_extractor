from openpyxl import load_workbook
import time
import logging

class excel:

    def __init__(self, input_xslx_file, output_xslx_file, insert_sheet_name):
        self.in_wb = load_workbook(input_xslx_file)
        self.output_xslx_file = output_xslx_file
        self.insert_sheet_name = "{}-{}".format(insert_sheet_name,time.strftime("%Y %d. %m. %H.%M.%S"))

    def get_column_values(self, sheet_name,url_column,skip_first_line=True):
        sheet = self.in_wb[sheet_name]
        urls = []
        for row in sheet:
            if row[0].row == 1 and skip_first_line:
                continue
            if row[url_column].value is None:
                break
            urls.append({"row_number": row[url_column].row , "url":row[url_column].value})
        return urls
    
    def get_parsers(self, sheet_name, skip_first_line=True):
        ws = self.in_wb[sheet_name]
        parsers = []
        for row in ws:
            if row[0].row == 1 and skip_first_line:
                continue
            if row[0].value is None or row[0].value == "":
                break
            cur_row = str(row[0].row)

            parsers.append(
                {'url_regex': ws['A'+cur_row].value, 
                'price_element': ws['B'+cur_row].value, 
                'verify_exists': ws['C'+cur_row].value,
                'verify_not_exists': ws['D'+cur_row].value})
        return parsers

    def save_in_excel(self, results):
        self.out_wb = load_workbook(self.output_xslx_file)
        self.out_wb.create_sheet(title=self.insert_sheet_name)
        ws = self.out_wb[self.insert_sheet_name]
        for parser_urls in results:
            for row in parser_urls["urls"]:
                ws.cell(row=row["row_number"], column=1, value=row["url"])
                ws.cell(row=row["row_number"], column=2, value=row["price"])
        while True:
            try:
                self.out_wb.save(self.output_xslx_file)
                break
            except:
                logging.info('Save failed. Retrying...')
                time.sleep(5)
        
