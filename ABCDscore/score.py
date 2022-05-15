import os
from urllib.parse import urlparse
import requests
import urllib.request
from bs4 import BeautifulSoup
from openpyxl import Workbook, load_workbook
import time
import csv

wb = load_workbook("C:/Users/arvid/Documents/xcel/test1.xlsx")
ws = wb.get_sheet_by_name('Sheet1')

#wordlist = load_workbook("c:/Users/arvid/Documents/GitHub/DEPI/WebsiteWordsScaper/wordlist_scrapper/wordlist.csv")

wbwrite = load_workbook("C:/Users/arvid/Documents/xcel/test.xlsx")
wbwritesheet = wbwrite.active

for row in ws.rows:
    os.remove(
        'c:/Users/arvid/Documents/GitHub/DEPI/WebsiteWordsScaper/wordlist_scrapper/wordlist.csv')
    URL = row[0].value
    print('#########################################################')
    print(URL)
    domain = urlparse(URL).netloc
    print(domain)
    print('#########################################################')
    os.system(
        f"cd C:/Users/arvid/Documents/GitHub/DEPI/WebsiteWordsScaper/wordlist_scrapper && scrapy crawl webcrawler -a start_url={URL} -a domains={domain} > wordlist.csv")

    with open('C:/Users/arvid/Documents/GitHub/DEPI/WebsiteWordsScaper/wordlist_scrapper/wordlist.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
          #TODO hier moet score berekend worden. -> opslaan in csv file ofzo
            print(line)