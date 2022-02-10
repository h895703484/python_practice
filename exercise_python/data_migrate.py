import time, json,re
import paramiko
import pymongo as pm
from bson.objectid import ObjectId

o_host='192.168.12.205'
o_port=29017
t_host='localhost'
t_port=27017

o_client = pm.MongoClient(host=o_host, port=o_port, authSource='cloud', username='cloud', password='Pass1234')
o_db = o_client['cloud']
t_client = pm.MongoClient(host=t_host, port=t_port, authSource='cloud', username='cloud', password='Pass1234')
t_db = t_client['cloud']

def model_migration(id):
    o_col=o_db['assets_model']
    t_col=t_db['assets_model']
    o_data=o_col.find_one({'_id': ObjectId(id)})
    t_col.insert_one(o_data)
    rules_migration(id)


def rules_migration(r_id):
    o_col = o_db['gather_rules']
    t_col = t_db['gather_rules']
    o_data = o_col.find({'model': r_id,'deleted':False})
    if o_data:
        for gr in o_data:
            t_col.insert(o_data)

if __name__=='__main__':
    mig_list=['6165182e0e79d00f8932cfb6','615fd5d5e6b51e3a2200f424','615fef2dd3234127e4528dc4','61516f30b0e85634846dd52f','6142de2f18807b6fa197ef4d','61396921965b4b0439a7974b']
    for _id in mig_list:
        model_migration(_id)
