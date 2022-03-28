from asyncio.windows_events import NULL
import json
from pickle import TRUE
import random
import time
from datetime import datetime
from warnings import catch_warnings
from openpyxl import Workbook, load_workbook


# test
def test():
    return ["test1","test2","test3"]


# reading xcel data 
readingXcel = False
loginfo = "staring"
def GetxcelData():
    global readingXcel
    global loginfo
    if(readingXcel is False):
        readingXcel = True
        #while True:
        try:
            #log that xcel is going to be red
            json_data = json.dumps({'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value':'Reading xcel' })
            loginfo = f"data:{json_data}\n\n"
            #get xcel
            wb = load_workbook("C:/Users/kevin/Documents/prioritieitenlijst.xlsx") # "C:/Users/arvid/Documents/xcel/ondernemingsnummers.xlsx"
            ws = wb.get_sheet_by_name('Oost-Vl') # West-Vl Antwerpen Limburg Vl-Brabant
            for row in ws.rows:
                json_data = json.dumps(
                    #{'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
                    {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value':  'ID: '+ str(row[0].value) + ',Naam: '+row[1].value + ',Gem: '+row[2].value })#
                loginfo = f"data:{json_data}\n\n"
                time.sleep(1)
        except:
            #log error 
            json_data = json.dumps({'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value':'Error during the reading of xcel' })
            loginfo = f"data:{json_data}\n\n"
            readingXcel = False


        


def GetxcelDataLogs():
    while True:
        global loginfo
        if(loginfo=="staring"):
            json_data = json.dumps({'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': "No process running"})
            loginfo = f"data:{json_data}\n\n"
        if(loginfo=="error"):
            json_data = json.dumps({'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': "error reading excel"})
            loginfo = f"data:{json_data}\n\n"
        yield loginfo
        time.sleep(1)

def GetxcelDataStarted():
    global readingXcel
    return readingXcel


