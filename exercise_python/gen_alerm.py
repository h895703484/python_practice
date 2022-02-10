import requests

url = "http://192.168.12.158:39094/v1/topics/device_data/messages"

payload = "{\"data\":[{\"key\":\"batteryDischarge\",\"value\": false},{\"key\": \"lostConn\", \"value\": false},{\"key\": \"noData\", \"value\": false}],\n\"did\": \"6019fc486b20b427eac07582\",\n\"mid\": \"60111f1a642fb92cbb780abf\", \n\"orgId\": \"admin\"}"
headers = {
    'content-type': "application/json",
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)