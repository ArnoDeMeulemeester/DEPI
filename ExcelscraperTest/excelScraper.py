from openpyxl import Workbook, load_workbook
import time

wb = load_workbook("C:/Users/arvid/Documents/xcel/ondernemingsnummers.xlsx")
ws = wb.get_sheet_by_name('Sheet1')


for row in ws.rows:
    print(row[0].value)
    time.sleep(1)