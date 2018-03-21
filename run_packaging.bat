pyinstaller --onefile run_extraction.py
copy phantomjs.exe dist
mkdir dist\excel
copy excel dist\excel
cd dist
run_extraction.exe
excel\out.xlsx
cd..
pause