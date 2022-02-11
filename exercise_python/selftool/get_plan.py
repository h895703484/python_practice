import json

with open('test.json','r',encoding='utf8') as f:
    data=json.load(f)


def get_planModelIdPath(l):
    for obj in l:
        planModelIdPath_list.append(obj.get("planModelIdPath"))
        if obj.get("childList"):
            get_planModelIdPath(obj["childList"])


if __name__ =="__main__":
    planModelIdPath_list=[]
    get_planModelIdPath(data)
    print(planModelIdPath_list)