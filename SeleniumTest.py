from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


print("Geef het ondernemingsnummer > ")
nummer = input()

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
 
driver.get("https://cri.nbb.be/bc9/web/catalog?execution=e1s1")

search = driver.find_element_by_id(
    "page_searchForm:j_id3:generated_number_2_component")
search.send_keys(nummer)
search.send_keys(Keys.RETURN)

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Download"))
    )
    element.click()
except:
    driver.quit()

