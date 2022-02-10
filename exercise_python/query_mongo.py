import time
import json
import paramiko
import pymongo as pm

host = '192.168.12.204'
port = 37017
myclient = pm.MongoClient(host=host, port=port, authSource='cloud', username='cloud', password='Pass1234')
mydb = myclient['cloud']


# 查询设备并返回所需列表
def find_device(sql):
    device_id_list = []
    my_col = mydb['assets_device']
    device_list = my_col.find(sql)
    for ele in device_list:
        device_id_list.append(str(ele.get('_id')))
    return json.dumps(device_id_list)


def find_unit(parentid_l):
    master_id_list = []
    my_col = mydb['assets_unit']
    for p_id in parentid_l:
        unit_list = my_col.find({"parentId": p_id, "branch": False})
        uid_list = [str(ele.get('_id')) for ele in unit_list]
        master_id_list.extend(uid_list)
    return json.dumps(master_id_list)


# 实时数据流未激活
def find_dfaf():
    did_list = []
    my_col = mydb['assets_dataflow']
    df_list = my_col.find({"isEnabled": False, "deleted": False})
    for df in df_list:
        did_list.append(df['source']['device'])
    return did_list


def update_df_status():
    t = paramiko.Transport('192.168.12.204', 22)
    t.connect(username='user', password='dacenT2017')
    sftp = paramiko.SFTPClient.from_transport(t)
    dir1 = '/home/user/opsdemo/dmock_demo/dmock3/data/'
    did_list=sftp.listdir(dir1)
    my_col = mydb['assets_dataflow']
    my_col.update_many({'$and': [{'source.device': {'$in': did_list}}, {'deleted': False}]},
                       {'$set': {"isEnabled": True}})


def cync_port():
    client_target = pm.MongoClient(host='192.168.12.8', port=28017, authSource='cloud', username='cloud', password='Pass1234')
    db_t = client_target['cloud']
    col_t = db_t['assets_dataflow']
    my_col = mydb['assets_dataflow']
    result = my_col.find({'deleted': False})
    for df in result:
        col_t.update_one({'deleted': False, 'source.device': df['source']['device']},
                         {'$set': {'connection.Info.port': df['connection']['Info']['port']}})


if __name__ == "__main__":
    # did=find_device({"params":{"$elemMatch":{"value":"60092f52e9b3ee599b2c4886"}},"type" : "5ed85e79b2bbd03994a43f27"})
    # did=find_unit(["60501dac57c8395cd8178d97", "605020af57c8395cd81793cf", "605020d557c8395cd81794f7", "6050210457c8395cd817961f", "6050213057c8395cd8179747"])
    # did = find_dfaf()
    # cync_port()
    update_df_status()
