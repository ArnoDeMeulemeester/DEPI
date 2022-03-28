# Testscenario van de tutorial

import requests
import urllib.request
from bs4 import BeautifulSoup
from openpyxl import Workbook, load_workbook

wb = load_workbook("C:/Users/arvid/Documents/xcel/workfile.xlsx")
ws = wb.get_sheet_by_name('Sheet1')
wbwrite = load_workbook("C:/Users/arvid/Documents/xcel/test.xlsx")
wbwritesheet = wbwrite.active
r = 1
c = 1

for row in ws.rows:
    naam = row[1].value
    naam = naam.replace(" ", "")
    print(naam)


# url site
    url = 'https://www.bing.com/search?q=' + naam + "+Belgie+Website"

# Connect to URL
    html = requests.get(url, headers={"User-Agent": "Requests"})
    obj = BeautifulSoup(html.text, "html.parser")
    link = obj.findAll('cite')[0].get_text()
    print(link)
    print("--------------------------------------")

    wbwritesheet.cell(row=r, column=c).value = link
    wbwrite.save("C:/Users/arvid/Documents/xcel/test.xlsx")

    r += 1
