from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox


#nummer = input("Geef het ondernemingsnummer: ")
ROOT = tk.Tk()
ROOT.withdraw()

nummer = simpledialog.askstring(title="Ondernemingsnummer",
                                prompt="Geef het ondernemingsnummer:")

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://cri.nbb.be/bc9/web/catalog?execution=e2s1")

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

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.ID, "j_idt131:j_idt165:0:generated_pdfDownload_0_cell"))
    )
    element.click()
finally:
    print("onderneming PDF gedownload")
    time.sleep(2)
    driver.quit()

messagebox.showinfo('Info', 'PDF download succesvol')
ROOT.mainloop()
