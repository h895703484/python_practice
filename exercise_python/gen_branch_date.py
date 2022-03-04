import time, json, re, random
import requests
import paramiko
import pymongo as pm
import pandas as pd
from bson.objectid import ObjectId

host = '192.168.12.89'
port = 27017
myclient = pm.MongoClient(host=host, port=port, authSource='cloud', username='cloud', password='Pass1234')
mydb = myclient['cloud']

unit_col = mydb['assets_unit']
device_col = mydb['assets_device']
deviceid_list = ['621f25f5ed748778be748aab','621f2178ed748778be748a62']

final_data = []


def get_params_list(groups):
    params_list = []
    for r_params in groups:
        if r_params['name'] in ['监测附加', '运行参数', '告警参数', '电能质量参数']:
            params_list += r_params['params']
    return params_list


def parse_param_type(p_data):
    res_value = None
    if isinstance(p_data, dict):
        p_type = p_data["type"]
    else:
        p_type = p_data["type"].values[0]

    if p_type == "boolean":
        res_value = random.choice([False, True])
    elif p_type == "enum":
        res_value = random.randint(0, len(p_data["enumValues"].values[0]) - 1)
    elif p_type == "string":
        res_value = "test_text"
    elif p_type == "number":
        res_value = random.randint(20, 50)
    elif p_type == "array":
        res_value = [1, 2, 3]
    return res_value


def get_params(model_id, category_id):
    device_pramas = []
    model_col = mydb['assets_model']
    cat_col = mydb['assets_category']
    if model_id:
        model_data = model_col.find_one({"_id": ObjectId(model_id)})
        pd_model_data = pd.DataFrame(model_data['params'])
    else:
        model_data = {'groups': []}
        pd_model_data = pd.DataFrame()
    cat_id = category_id
    cat_data = cat_col.find_one({'_id': ObjectId(cat_id)})
    pd_cat_data = pd.DataFrame(cat_data['params'])

    params_list = get_params_list(cat_data['groups']) + get_params_list(model_data['groups'])
    for param_id in params_list:
        pc_data = pd_cat_data[pd_cat_data['id'] == param_id]
        pm_data = pd_model_data[pd_model_data['id'] == param_id] if not pd_model_data.empty else pd_model_data
        if pm_data.empty:
            if pc_data["type"].values[0] == "table":
                pass
                # for p in pc_data["tableData"].values[0]:
                #     p_value = parse_param_type(p)
                #     device_pramas.append({"key": p["code"], "name": p["name"], "value": p_value})
            else:
                key = pc_data["code"].values[0]
                name = pc_data["name"].values[0]
                value = parse_param_type(pc_data)
                device_pramas.append({"key": key, "value": value, "name": name})
        else:
            if pm_data["type"].values[0] == "table":
                pass
                # for p in pm_data["tableData"].values[0]:
                #     p_value = parse_param_type(p)
                #     device_pramas.append({"key": p["code"], "name": p["name"], "value": p_value})
            else:
                key = pm_data["code"].values[0]
                name = pm_data["name"].values[0]
                value = parse_param_type(pm_data)
                device_pramas.append({"key": key, "value": value, "name": name})

    return {"data": device_pramas, "mid": model_id}


def get_data(res):
    for unit in res:
        device = device_col.find_one({'_id': ObjectId(unit['parentId'])}) if unit.get('parentId') else unit
        deviceName = device['name'] + unit['name']
        array = [{'key': 'electricity', 'value': random.randint(20, 30)}]
        did = str(unit['_id'])
        mid = unit.get('model', '')
        ownId = 'admin'
        # data = "// " + deviceName + ' \n  socket.emit("device_data", {"id": Date.now(), "data":' + json.dumps(
        #     array,ensure_ascii=False) + ', "did": "' + did + '", "mid": "' + mid + '", "orgId": "' + ownId + '"})'+'\n'
        # final_data.append(data)
        res = get_params(mid, unit['type'])
        res["did"] = did
        res["orgId"] = ownId
        res["name"] = unit['name']
        final_data.append(res)


# with open("branch_data.json","a",encoding='utf8') as f:
#     for d in final_data:
#         f.write(d)
if __name__ == "__main__":
    res_unit = unit_col.find({'$or': [{'parentId': d_id} for d_id in deviceid_list]})
    res_device = device_col.find({'$or': [{'_id': ObjectId(d_id)} for d_id in deviceid_list]})
    get_data(res_unit)
    get_data(res_device)
    with open("device_data.json", "w", encoding='utf8') as f:
        json.dump(final_data, f, indent=4, ensure_ascii=False)
