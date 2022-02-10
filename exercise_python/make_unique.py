brands=['hp','dell','dell','lenovo','dell']
for i in range(len(brands)-1,0-1,-1):
    if brands.count(brands[i])>1:
        brands.pop(i)
print(brands)