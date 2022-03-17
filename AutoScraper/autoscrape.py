from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from openpyxl import Workbook, load_workbook




wb = load_workbook("C:/Users/arvid/Documents/xcel/ondernemingsnummers.xlsx")
ws = wb.get_sheet_by_name('Sheet1')


for row in ws.rows:
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    
    print(row[0].value)
    nummer = row[0].value
    nummer = nummer.replace(" ", "")
    print(nummer)

    driver.get(
        "https://cri.nbb.be/bc9/web/catalog?execution=e1s1")

    try:
        element1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, "page_searchForm:j_id3:generated_number_2_component"))
        )
        search = driver.find_element_by_id(
            "page_searchForm:j_id3:generated_number_2_component")
        search.send_keys(nummer)
        search.send_keys(Keys.ENTER)
    finally:
        print("Onderneming opzoeken was succesvol")
        time.sleep(5)
        driver.quit()

    time.sleep(2)
