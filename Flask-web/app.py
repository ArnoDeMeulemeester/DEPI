from asyncio.windows_events import NULL
from distutils.log import debug
from flask import Flask, render_template, request, url_for, Response, stream_with_context
from xlReader import test,GetxcelDataLogs,GetxcelData,GetxcelDataStarted
from sqlFuncions import translate_search_to_sql
import json
import random
import time
from datetime import datetime
import pymysql
import selenium 
import pandas as pd
from sshtunnel import SSHTunnelForwarder

app = Flask(__name__)
# SSH tunnel
tunnel = SSHTunnelForwarder(
    ('vichogent.be',40006),
    ssh_username = 'root',
    ssh_password = 'change-me-48io23as',
    remote_bind_address=('127.0.0.1',3306)
)
tunnel.start()
# MYSQL returns pandas dataframe
def _MYSQL(query):
    conn = pymysql.connect(host='127.0.0.1', user='root',
    passwd='@Groep8depi', db='dep',
    port=tunnel.local_bind_port)
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

# Routing
@app.route('/sqlTest')
def sqlTest():
    #data = _MYSQL('''SELECT VERSION();''')
    data = _MYSQL('''SELECT * FROM dep.KMO;''')
    return str(data.iloc[0])

# KMO Overview pages 
@app.route('/KMOOverview')
def KMOOverviewBase():
    db_data_KMO = _MYSQL('''SELECT * FROM dep.KMO limit 100;''')
    db_data_KMO.set_index('onderneminsNr',inplace=True)
    db_data_sector = _MYSQL('''SELECT * FROM dep.Sector limit 100;''')
    db_data_sector.set_index('sectorID',inplace=True)
    #return db_data_KMO.to_json(orient="index",force_ascii=True,index=True)
    return render_template('KMO_overview.html', kmo_data=db_data_KMO.to_json(orient="index",force_ascii=True,index=True), sector_data=db_data_sector.to_json(orient="index",force_ascii=True,index=True), baseurl=request.base_url)
    #return render_template('KMOOverview.html', tables=[db_data.to_html(classes='data')], titles=db_data.columns.values)

# KMO Overview pages 
@app.route('/SectorOverview')
def SectorOverviewBase():
    db_data_sector = _MYSQL('''SELECT * FROM dep.Sector limit 100;''')
    db_data_sector.set_index('sectorID',inplace=True)
    return render_template('sector_overview.html', sector_data=db_data_sector.to_json(orient="index",force_ascii=True,index=True), baseurl=request.base_url)



# Sector Overview pages

# Get location Info
@app.route('/getLocationInfo/<path:path>')
def GetLocationByID(path):
    ID = path.replace("%20", " ")
    db_data = _MYSQL('''SELECT * FROM dep.Locatie WHERE adres='{}';'''.format(ID))
    return db_data.to_json(orient="index",force_ascii=True,index=True)

# Get Balans info
@app.route('/getBalansInfo/<path:path>')
def GetBalansByID(path):
    ID = path.replace("%20", " ")
    db_data = _MYSQL('''SELECT * FROM dep.Balans WHERE bvdIDnr='{}';'''.format(ID))
    return db_data.to_json(orient="index",force_ascii=True,index=True)

# multi select querry
@app.route('/search/KMO', methods = ['GET', 'POST'])
def searchKMOs(): 
    raw_data = request.get_json()
         
    
    db_data_KMO = _MYSQL(translate_search_to_sql(raw_data))
    db_data_KMO.set_index('onderneminsNr',inplace=True)
    # check if need to reorder
    return db_data_KMO.to_json(orient="index",force_ascii=True,index=True)
    #return sql_statement


# Test Pages
@app.route('/SectorOverview')
def SectorOverviewTest():
    db_data = _MYSQL('''SELECT * FROM dep.Sector;''')
    return render_template('KMOOverview.html', tables=[db_data.to_html(classes='data')], titles=db_data.columns.values)

 
@app.route('/ImportFromXcel')
def ImportFromxl():
    return render_template('ImportFromxl.html', baseurl=request.base_url)

@app.route('/ImportFromXcel/GetProgress')
def XcelData():
    response = Response(stream_with_context(GetxcelDataLogs()), mimetype="text/event-stream")   
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

@app.route('/ImportFromXcel/StartProgress')
def XcelDatastart():
    if(GetxcelDataStarted() is False):
        GetxcelData()
        return "started"
    else:
        return "Already running"


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)