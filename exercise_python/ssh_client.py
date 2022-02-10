import re,json
import time
import paramiko
import pandas as pd


client=paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('192.168.12.205',22,'user','dacenT2017')
stdin,stdout,stderr=client.exec_command('cd ~/opsdemo && cat dmock/config/config.json')
o_data=stdout.read().decode('utf-8')
print(o_data)
data=json.loads(o_data)
df=pd.DataFrame(data["servers"])
t_port=df[df.dir=='./data/yuzhufeng-ups2']['port']
print(t_port.values)
client.close()

# t = paramiko.Transport('192.168.12.205', 22)
# t.connect(username='user', password='dacenT2017')
# sftp = paramiko.SFTPClient.from_transport(t)
# dir1 = '/home/user/dmock_demo/dmock3/data/'
# res = sftp.listdir(dir1)
# for x in res:
#     if re.match('^6',x):
#         dir2 = dir1 + x
#         res1 = sftp.listdir(dir2)
#         for y in res1:
#             f1 = y.split('.')
#             if re.search('[a-z]',f1[0]):
#                 f1[0] = f1[0].upper()
#                 f2 = '.'.join(f1)
#                 old = dir2 + '/' + y
#                 new = dir2 + '/' + f2
#                 if old != new:
#                     sftp.rename(old, new)
#                 time.sleep(1)
#         res2 = sftp.listdir(dir2)
#         print(x, res2)
