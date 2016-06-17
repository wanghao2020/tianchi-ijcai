import numpy as np
import csv

originResult = '/home/wanghao/Document/tianchi/result/5-20/skGBDTresult4_sample.csv'
afterResult = '/home/wanghao/Document/tianchi/result/5-20/skGBDTresult3_sample.csv'

wfile = open(afterResult, 'wb')
writer = csv.writer(wfile)

with open(originResult, 'rb') as f :
    for line in f :
        line = line.strip('\r\n')

        user,location,merchant = line.split(',')

        merchants = merchant.split(':')
        threeMerchant = merchants[0:3]
        str = ''
        for mer in threeMerchant:
            str = str + mer + ':'
        str = str[0: len(str) - 1]

        one = []
        one.append(user)
        one.append(location)
        one.append(str)
        writer.writerow(one)

wfile.close()