from dataMethod import data
import random
import csv

## model for predicting
data = data()
testfile = data.koubeitest_path
data.inputdata()
location_merchant = data.location_merchant
allResult = []

with open(testfile,'rb') as f :
    count = 0
    for line in f :
        linelist = line.split(',')
        result = [linelist[0],linelist[1][0:len(linelist[1])-1]]

        merchantlist = location_merchant[int(linelist[1])]
        string = ''
        if len(merchantlist) <= 10 :
            for merchant in merchantlist:
                string = string + str(merchant) + ':'
            string = string[0:len(string)-1]
            print string
            result.append(string)
        else:
            # random
            merchantlist = random.sample(merchantlist,10)
            for merchant in merchantlist:
                string = string + str(merchant) + ':'
            string = string[0:len(string) - 1]
            print string
            result.append(string)

        allResult.append(result)

csvfile = '/home/wanghao/Document/tianchi/result/result.csv'
with open (csvfile,'wb') as f :
    writer = csv.writer(f)
    writer.writerows(allResult)



