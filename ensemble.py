# get the result ensemble
import csv

modelresult1 = '/home/wanghao/Document/tianchi/result/newvisitedresult.csv'
modelresult2 = '/home/wanghao/Document/tianchi/result/5-21/RFresult3.csv'
ensembleresult = '/home/wanghao/Document/tianchi/result/5-21/newensembel_sample.csv'

readfile1 = open(modelresult1, 'rb')
readfile2 = open(modelresult2, 'rb')
writerfile = open(ensembleresult, 'wb')
writer = csv.writer(writerfile)
data1 = readfile1.readlines()
data2 = readfile2.readlines()

lines = len(data1)



for i in range(lines):

    result = []

    result1 = data1[i].strip('\r\n')
    result2 = data2[i].strip('\r\n')

    user1,location1,merchants1 = result1.split(',')
    user2,location2,merchants2 = result2.split(',')

    merchant1 = merchants1.split(':')
    merchant2 = merchants2.split(':')

    set1 = set(merchant1)
    set2 = set(merchant2)

    finalresult = set1 & set2

    str = ''
    for mer in finalresult:
        str = str + mer + ':'
    str = str[0 : len(str) - 1]

    result.append(user1)
    result.append(location1)
    result.append(str)

    writer.writerow(result)

writerfile.close()