import time, re, json
import pymongo as pm
from bson.objectid import ObjectId


def get_room_id(params):
    for p in params:
        if p.get('code') == 'room':
            return p.get('value')


def add_data(rid, model, device_id):
    c_data = device_id_doc.get(rid)
    if c_data:
        if c_data.get(model) == None:
            c_data[model] = [device_id]
        else:
            c_data[model].append(device_id)
        return c_data
    else:
        return {model: [device_id]}


def get_room_name(rid):
    room_doc = room_col.find_one({'_id': ObjectId(rid)})
    room_name = room_doc.get('name')
    return room_name

def get_model_name(mid):
    model_doc = models.find_one({'_id': ObjectId(mid)})
    model_name = model_doc.get('name')
    return model_name


host = '192.168.12.157'
port = 27017
myclient = pm.MongoClient(host=host, port=port, authSource='cloud', username='cloud', password='Pass1234')
mydb = myclient['cloud']
device_id_doc = {}
room_col = mydb['assets_room']
models=mydb['assets_model']
col = mydb['assets_device']
res = col.find({'$and': [{'deleted': False},
                         {'$or': [{'type': '5bd90a951c9d4433e60f2b25'}, {'type': '6008da15a418c0157dd5189c'},{'type':'5ed85e79b2bbd03994a43f27'}]}]})
for doc in res:
    room_id = get_room_id(doc.get('params'))
    room=get_room_name(room_id)
    model=get_model_name(doc.get('model'))
    device_id_doc[room] = add_data(room, model, str(doc.get('_id')))

with open('device_id.json', 'w', encoding='utf8') as f:
    json.dump(device_id_doc, f, indent=4,ensure_ascii=False)
