import time, json, re
import paramiko
import pandas as pd
import pymongo as pm

host = '192.168.12.205'
port = 28018

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('192.168.12.206', 22, 'user', 'dacenT2017')
stdin3, stdout3, stderr3 = client.exec_command('cd /home/user/dmock_demo/dmock3/config && cat config.json')
o3_data = stdout3.read().decode('utf-8')
# stdin5, stdout5, stderr5 = client.exec_command('cd /home/user/dmock_demo/dmock5/config && cat config.json')
# o5_data = stdout3.read().decode('utf-8')
dmock_json = pd.DataFrame(json.loads(o3_data)["servers"])
# dmock_json[dmock_json['dir']== "./data/600a31365b8b75655ed68f8"]["port"].values

myclient = pm.MongoClient(host=host, port=port, authSource='cloud', username='cloud', password='Pass1234')
mydb = myclient['cloud']

mycol_name = mydb.list_collection_names()

col = mydb['assets_dataflow']
col2 = mydb['acqunit']
res = col.find({'deleted': False})
pattern = re.compile('^\d+')

for r1 in res:
    did = r1["source"]["device"]
    port = dmock_json[dmock_json['dir'] == f"./data/{did}"]["port"].values
    if r1['connection']['Info']['address'] == '192.168.12.206':
        p = port[0] if port.any() else r1['connection']['Info']['port']
        col.update_many({'$and': [{'source.device': did}, {'deleted': False}]},
                        {'$set': {'connection.Info.port': f'{p}', 'connection.Info.address': '192.168.12.206',
                                  "isEnabled": True}})
        col2.update_many({'asset.id': did}, {
            '$set': {'connection.port': f'{p}', 'connection.address': '192.168.12.206', "enable": True}})
    else:
        continue
    # col.update_one({'source.device': did}, {'$set': {'connection.Info.address': '192.168.12.205'}})
