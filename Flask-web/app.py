from distutils.log import debug
from flask import Flask, render_template, request, url_for, Response, stream_with_context
from xlReader import test,GetxcelDataLogs,GetxcelData,GetxcelDataStarted
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


@app.route('/KMOOverview')
def KMOOverviewTest():
    db_data = _MYSQL('''SELECT * FROM dep.KMO;''')
   # return render_template('KMOOverview.html', data=db_data)
    return render_template('KMOOverview.html', tables=[db_data.to_html(classes='data')], titles=db_data.columns.values)

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