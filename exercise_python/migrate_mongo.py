import time
import json
import os
import pymongo as pm

host = '192.168.12.205'
port = 28017
myclient = pm.MongoClient(host=host, port=port, authSource='cloud', username='cloud', password='Pass1234')
mydb = myclient['cloud']

# o_myclient = pm.MongoClient(host='192.168.12.155', port=27017, authSource='cloud', username='cloud', password='Pass1234')
# o_mydb = o_myclient['cloud']

mycol_name = mydb.list_collection_names()
# ocol_name = o_mydb.list_collection_names()
# print(len(ocol_name))
# dif_list=[]
# for name in mycol_name:
#     if name not in ocol_name:
#         dif_list.append(name)
# print(dif_list)

# os.system(f"del {' '.join(mycol_name)}")

for col_name in mycol_name:
    print(col_name)
    os.system(f"mongoexport -h 192.168.12.205:28017 -d cloud -c {col_name} -o {col_name+'.dump'}")
    time.sleep(3)
    os.system(f"mongoimport -h 192.168.12.155:27017 -u cloud -p Pass1234 -d cloud -c {col_name} {col_name+'.dump'}")
    time.sleep(1)
    os.system(f"del {col_name+'.dump'}")



