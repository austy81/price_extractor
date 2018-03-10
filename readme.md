Price extractor

workflow:
- Program needs excel file named in.xlsx which is in subdirectory excel.
- Excel contains tabs with sheets: urls and settings
- urls contains in first column url addresses. 
- price_extractor will extract prices from given urls
- settings sheet contains setup of scrapers
- PhantomJS is web browser used for automation
- to start extraction run run_extraction.exe
- you will see progress in console vindow
- there will be log entry after each finished parser
- final results will be saved in out.xlsx file in subdirectory excel
- program will create for results new tab containing current date and time
- now you can admire ROBO work ;-)