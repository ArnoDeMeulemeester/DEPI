from distutils.log import debug
from flask import Flask, render_template, request, url_for, Response, stream_with_context
from xlReader import test,GetxcelDataLogs,GetxcelData,GetxcelDataStarted
import json
import random
import time
from datetime import datetime
import selenium 

app = Flask(__name__)



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


@app.route('/')
def index():
    return render_template('index.html')
    

if __name__ == "__main__":
    app.run(debug=True)