import json, traceback,re,collections
import paramiko

dir='E:/opsdemo/aiowrapp/'
with open('config.production.json', encoding='utf8') as f:
    config_o = f.read()

with open('aio_config_map.json', encoding='utf8') as m:
    config_m = json.load(m,object_pairs_hook=collections.OrderedDict)


def modify_config(o, m):
    try:
        o = o if isinstance(o, str) else str(o)
        for i, j in sorted(m.items(), key=lambda x: x[0]):
            o = o.replace(i, j if j else i)
        o=o.replace(re.findall('("buzlog": .*"debug".{1,20},).*"performance"',o,re.S)[0],'')
        return o
    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    res_content = modify_config(config_o, config_m)
    # res_buz=re.findall('("buzlog": .*"debug".{1,20},.).*"performance"',res_content,re.S)
    # print(res_buz)
    res_content=json.loads(res_content,object_pairs_hook=collections.OrderedDict)
    res_content['pueConifg']= '' if res_content.get('pueConifg') else res_content.get('pueConifg')
    # if res_content:
    #     with open('E:/opsdemo/aiowrapp/config.production.json', 'w', encoding='utf8') as w:
    #         json.dump(res_content,w,indent=4)
    #         print('配置文件修改成功')
    print(res_content)
