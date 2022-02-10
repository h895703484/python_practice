import json
import requests
import asyncio
import time
from threading import Timer

with open("device_data.json", "r", encoding='utf8') as f:
    device_data = json.load(f)
url = "http://192.168.12.157:49094/v1/topics/device_data/messages"


# async def send_data():
#     requests.post(url=url,data=)
def send_data():
    for data in device_data:
        requests.post(url=url, json=data)
    # t = Timer(5, send_data)
    # t.start()


def send_lostConn():
    for data in device_data:
        data["data"] = [{"key": "lostConn", "value": False}]
        requests.post(url=url, json=data)


def send_noData():
    for data in device_data:
        data["data"] = [{"key": "noData", "value": False}]
        requests.post(url=url, json=data)


if __name__ == "__main__":

    send_data()
    # send_lostConn()
    # send_noData()
