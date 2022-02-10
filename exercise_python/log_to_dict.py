with open('result.log', 'r', encoding='utf8') as log:
    log_list = log.readlines()
    key_list = log_list[5].split('\t')
    key1 = key_list[0].replace('\n', '')
    key2 = key_list[2].replace('\n', '')
    key3 = key_list[3].replace('\n', '')
    key4 = key_list[4].replace('\n', '')
    data_dict = {key1: [], key2: [], key3: [], key4: []}
    for values in log_list[6:-2]:
        values_list = values.split('\t')
        data_dict[key1].append(values_list[0].replace('\n', ''))
        data_dict[key2].append(values_list[1].replace('\n', ''))
        data_dict[key3].append(values_list[2].replace('\n', ''))
        data_dict[key4].append(values_list[3].replace('\n', ''))

import re
pattern=r'(^0(,0){9,}|(,0){10,})'
data=','.join(list_)
result=re.search(pattern,data)
result.group(1).count('0')