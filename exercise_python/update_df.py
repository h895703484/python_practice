import time, json, re
import paramiko
import pymongo as pm

host = '192.168.12.156'
port = 27017
myclient = pm.MongoClient(host=host, port=port, authSource='cloud', username='cloud', password='Pass1234')
mydb = myclient['cloud']
mycol_name = mydb.list_collection_names()
config = []
col = mydb['assets_dataflow']
col2 = mydb['acqunit']


def get_device_list():
    t = paramiko.Transport('192.168.12.206', 22)
    t.connect(username='user', password='dacenT2017')
    sftp = paramiko.SFTPClient.from_transport(t)
    dir1 = '/home/user/dmock_demo/dmock3/data/'
    res_data = sftp.listdir(dir1)
    return res_data


def update_df_data():
    res_data = get_device_list()
    res = col.find({'deleted': False})
    p = 17000
    pattern = re.compile('^\d+')
    for r1 in res:
        cof = {}
        did = r1["source"]["device"]
        cof["type"] = r1['point']['protocolType'] if r1['point']['protocolType'] != 'customDrivers' else "private"
        cof['dir'] = f'./data/{did}'
        cof['port'] = str(p)
        config.append(cof)

        # col.update_one({'source.device':did},{'$set':{'connection.Info.address':'192.168.12.205'}})
        if not r1.get('connection', {}).get('Info', {}).get('address'):
            continue
        if '192.168.40' in r1['connection']['Info']['address'] and did in res_data:
            col.update_many({'$and': [{'source.device': did}, {'deleted': False}]},
                            {'$set': {'connection.Info.port': f'{p}', 'connection.Info.address': '192.168.12.206',
                                      "isEnabled": True}})
            col2.update_many({'asset.id': did}, {
                '$set': {'connection.port': f'{p}', 'connection.address': '192.168.12.206', "enable": True}})
            p += 1
        else:
            col.update_many({'$and': [{'source.device': did}, {'deleted': False}]},
                            {'$set': {
                                "isEnabled": False}})
            col2.update_many({'asset.id': did}, {
                '$set': {"enable": False}})


# print(config)
# print(len(config))

def update_df_status():
    col.update_many({},
                    {'$set': {"isEnabled": False}})
    col2.update_many({}, {
        '$set': {"enable": False}})


if __name__ == "__main__":
    # update_df_status()
    update_df_data()
    with open('config.json', 'w', encoding='utf8') as f:
        json.dump(config, f, indent=4)

# col.update({},{'$set':{'deleted':False}},multi=True)
