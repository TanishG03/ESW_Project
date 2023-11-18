from flask import Flask, render_template, send_from_directory, jsonify
from random import randint
from requests import request
import random
import json

def getDroneSensorsData():
    url = "http://192.168.214.64:8080/~/in-cse/in-name/DroneSensing/Drone-1/Data/?rcn=4"

    payload = {}
    headers = {
        'X-M2M-Origin': 'admin:admin',
        # 'Accept': 'application/json'
        'Content-Type': 'application/json;ty=4'
    }
    response = request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        data = json.loads(response.text)

        cin_list = data["m2m:cnt"]["m2m:cin"]
        result = []
        for cin_entry in cin_list:
            con_value = cin_entry.get("con")

            if con_value:
                result.append(con_value)
        # print(result)
        # Template of this data :[Temperature, Humidity, AQI, Altitude]
        ans = []
        for item in result:
            r = json.loads(item)
            ans.append(r)
        data = {}
        data['droneSensors'] = ans[5:]
        # print(data)
        return data
    
    elif response.status_code == 401:
        print("Unauthorized request. Check your authentication credentials.")
    elif response.status_code == 404:
        print("Requested resource not found.")
    else:
        print("Error:", response.status_code)
        
        


# Initialize global variable





app = Flask(__name__)

@app.route("/")
def load_homepage():
    return render_template('index.html')

@app.route("/about")
def load_about():
    return render_template('about.html')

@app.route("/hardware")
def load_hardware():
    return render_template('hardware.html')

@app.route("/analytics")
def load_analytics():
    return render_template('analytics.html')

@app.route("/showData")
def load_data():
    rawData = getDroneSensorsData()
    return render_template('data_page.html', sensorData=rawData)
    
 
# @app.route("/display")
#def load_display():
  #  return render_template('display.html', sensorData = 
global_realtime_data = None
data = {
        "val1": random.randint(1,90),
        "val2": random.randint(1,90),
        "val3": random.randint(1,90)
    }
global_realtime_data = data

@app.route("/esp32-data", methods=['POST'])
def handle_request():
    global global_realtime_data  # Declare global variable
    data = request.get_json()
    print("Data Received:", data)
    
    data = {
        "val1": random.randint(1,90),
        "val2": random.randint(1,90),
        "val3": random.randint(1,90)
    }
    global_realtime_data = data
    print("Data Received:", data)
    return "Data received"

@app.route('/realtime')
def render_realtime_data():
    # Check if global_realtime_data is not None before rendering
    if global_realtime_data is not None:
        return render_template('realtime.html', data=global_realtime_data)
    else:
        return "No realtime data available."


@app.route("/get_data")
def get_data():
    raw_data = getDroneSensorsData()
    return jsonify(sensorData=raw_data)


# @app.route("/")
# def data_page():
#     raw_data = getDroneSensorsData()
#     return render_template('data_page.html', sensorData=raw_data)


@app.route('/<path:path>')
def send_report(path):
    return send_from_directory('./', path)


app.run(host='0.0.0.0', port=5001) 
