import random

target_num=random.randint(1,101)
print(target_num)
min_num=0
max_num=100
count=0
while True:
    input_num = input('请输入1～100的整数：')
    count+=1
    if not input_num.isdigit():
        print('非法输入')
        continue
    if int(input_num)>100 or int(input_num)<0:
        print('非法输入')
        continue
    if int(input_num)>target_num:
        max_num=int(input_num) if int(input_num)<max_num else max_num
        print(f'比{input_num}小，请输入{min_num}～{max_num}之间的数字')
    if int(input_num)<target_num:
        min_num=int(input_num) if int(input_num)> min_num else min_num
        print(f'比{input_num}大，请输入{min_num}～{max_num}之间的数字')
    if int(input_num)==target_num:
        print('正确',f'共猜了{count}次')
        break


