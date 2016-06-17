# coding=utf-8

# ----------------------------- user koubei feature

# ----------------------------- uesr taobao feature

# ----------------------------- merchant feature

# ----------------------------- user and merchant feature


file = '/home/wanghao/RFresult0.35'

count0 = 0
count11 = 0

with open(file, 'rb') as f :
    for line in f :
        line = line.strip('\r\n')
        user,location,merchant = line.split(',')
        merchants = merchant.split(':')
        if len(merchant) == 0 :
            count0 += 1
        if len(merchants) > 5 :
            count11 += 1

print '0 merchants, ',count0
print '>10 merchants ', count11