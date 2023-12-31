from flask import Flask, render_template, send_from_directory
from random import randint
from requests import request
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
        print("=======================")
        data = {}
        data['droneSensors'] = ans[:5]
        print(data)
        return data
    
    elif response.status_code == 401:
        print("Unauthorized request. Check your authentication credentials.")
    elif response.status_code == 404:
        print("Requested resource not found.")
    else:
        print("Error:", response.status_code)

getDroneSensorsData()
