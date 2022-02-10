import requests
import json
import time

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Im1vbml0b3JfcGF0cm9sIiwiYWNjb3VudElkIjoic3h4aCIsImlmTmVlZFJlZnJlc2giOmZhbHNlLCJpYXQiOjE2MzkxMjM3MTAsImV4cCI6MTYzOTIxMDExMH0.741g3dtvUFbpdjvWCHyiS9wcah5aKi5P8BEir10PL5M"
}


def get_config(version=""):
    data = {"version": "1.0",
            "data": {"version": version}
            }
    res = requests.post('http://192.168.12.158:3366/north/config_get', data=json.dumps(data), headers=headers)
    res_json = json.loads(res.text)
    if res_json.get("error_code") == 0:
        with open("device.json", "w", encoding="utf8") as f:
            json.dump(res_json, f, ensure_ascii=False, indent=4)
    return res.text


def get_offline_alerm(begin_time=int(time.time() * 1000) - 3600 * 24 * 10 * 1000, end_time=int(time.time() * 1000),
                      size=1000):
    data = {
        "version": "1.0",
        "data": {
            "begin_time": begin_time,
            "end_time": end_time,
            "pager": {"index": 1, "size": size},
            "sorter": {"triggerTime": "desc"}
        }
    }

    res = requests.post("http://192.168.12.158:3366/north/offline_alarm_get", data=json.dumps(data), headers=headers)
    res_json = json.loads(res.text)
    alerm_num[0] = res_json.get("data")["count"] if res_json.get("data") else 0
    if res_json.get("error_code") == 0:
        with open("north_alerm.json", "w", encoding="utf8") as f:
            json.dump(json.loads(res.text), f, ensure_ascii=False, indent=4)
    return res.text


def get_online_data(device_guids=None, point_guids=None):
    if device_guids is None:
        device_guids = []
    if point_guids is None:
        point_guids = []
    data = {
        "version": "1.0",
        "data": {
            "space_guids": None,
            "device_guids": device_guids,
            "point_guids": point_guids
        }
    }
    res = requests.post("http://192.168.12.158:3366/north/online_data_get", data=json.dumps(data), headers=headers)
    res_json = json.loads(res.text)
    if res_json.get("error_code") == 0:
        with open("north_data.json", "w", encoding="utf8") as f:
            json.dump(json.loads(res.text), f, ensure_ascii=False, indent=4)
    return res.text


def get_units(unit):
    if unit.get("units"):
        for y in unit["units"]:
            get_units(y)
            device_id_list.append(y["guid"])
            get_deviceId_and_params(y)


def get_deviceId_and_params(device):
    if not device.get("nodes"):
        return
    for x in device["nodes"]:
        if x.get("space_type") == "room":
            room_name.append(x["name"])
        if not x.get("node_type"):
            device_name.append(x["name"])
            device_id_list.append(x["guid"])
        if x.get("node_type") == 3:
            params_list.append(x["tag"])
        # if x.get("units"):
        #     for y in x["units"]:
        #         device_id_list.append(y["guid"])
        #         get_deviceId_and_params(y)
        get_units(x)
        get_deviceId_and_params(x)


def get_deviceId():
    with open("device.json", "r", encoding="utf8") as f:
        data = json.load(f)
        get_deviceId_and_params(data["data"])


def append_result(res):
    with open("result.json", "a", encoding="utf8") as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=4) + ',' + '\r\n')


def count_pramas():
    num = 0
    with open("north_data.json", "r", encoding="utf8") as f:
        data = json.load(f)
        for dp in data['data']['devices']:
            num += len(dp["points"] if dp.get('points') else [])
    return num


if __name__ == "__main__":
    interface_dict = {"get_config": [get_config, "config_get"],
                      "get_offline_alerm": [get_offline_alerm, "offline_alarm_get"],
                      "get_online_data": [get_online_data, "online_data_get"]}
    room_name = []
    device_name = []
    device_id_list = []
    params_list = []
    start_time = time.time()
    alerm_num = [None]
    alerm_size = 100
    get_deviceId()
    res_device = interface_dict["get_online_data"][0](device_guids=device_id_list, point_guids=list(set(params_list)))
    # res_alerm = get_offline_alerm()
    # res_data = get_online_data()
    end_time = time.time()
    # get_deviceId()
    use_time = end_time - start_time
    # params_num = count_pramas()
    test_result = {"interface": interface_dict["get_online_data"][1], "Time use(s)": round(use_time, 2),
                   "permissions": ','.join(room_name),
                   "parmas_num": len(params_list), "device_total_num": int(len(device_id_list)),
                   "device_num": len(device_name), "total_alerm_num": alerm_num[0],
                   "alerm_num": alerm_size}
    # append_result(test_result)
    print(res_device)
