import time
import json
import pymongo as pm

host = '192.168.12.204'
port = 37017
myclient = pm.MongoClient(host=host, port=port, authSource='cloud', username='cloud', password='Pass1234')
mydb = myclient['cloud']

mycol_name = mydb.list_collection_names()

for col_name in mycol_name:
    print(col_name)
    col=mydb[col_name]
    # col.drop()
    res=col.delete_many({'deleted':True})
    print(res.deleted_count,'个文档已删除')


# col.update({},{'$set':{'deleted':False}},multi=True)


