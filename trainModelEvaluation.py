import numpy as np
from sklearn.externals import joblib
import csv
import time
import sys

trainfeature = np.load('./trainfeature.npy')
trainlabel = np.load('./trainlabel.npy')
trainpairfile = './trainpair'
trainpair = []
with open(trainpairfile, 'rb') as f :
    for line in f :
        line = line.strip('\r\n')
        user,merchant,location = line.split(',')
        trainpair.append((user,merchant,location))

model = joblib.load('sampleRFmodel.pkl')
y_pred = model.predict_proba(trainfeature)
trainResult = {}
for i in range(len(y_pred)):
    trainResult[trainpair[i]] = y_pred[i][1]

# get the location_ merchants data
merchantinfo = '/home/wanghao/model/ijcai2016_merchant_info'
location_merchants = {}
with open(merchantinfo, 'rb') as f :
    for line in f :
        line = line.strip('\r\n')
        merchant, budget, location = line.split(',')
        locations = location.split(':')
        for loc in locations :
            if not location_merchants.has_key(loc):
                location_merchants[loc] = []
            location_merchants[loc].append(merchant)

testfile = '/home/wanghao/model/train_UL'
resultfile = '/home/wanghao/model/result/trainsampleresult'
writefile1 = open(resultfile, 'wb')
write1 = csv.writer(writefile1)


thresold = 0.20
with open(testfile, 'rb') as f:
    count = 0
    for line in f :
        count += 1
        sys.stdout.write('\rtest current count %d'%count)
        sys.stdout.flush()

        result = []

        line = line.strip('\r\n')
        user,location = line.split(',')

        result.append(user)
        result.append(location)


        merchant_prob = {}

        for merchant in location_merchants[location]:
                merchant_prob[(user,merchant,location)] = trainResult[(user,merchant,location)]

        merchant = []
        for key in merchant_prob.keys():
            if merchant_prob[key] > thresold:
                merchant.append(key[1])

        if len(merchant) == 0:
            sortedMerchant = sorted(merchant_prob.iteritems(), key=lambda d: d[1],reverse=True)[0:2]
            merchant.append(sortedMerchant[0][0][1])
            merchant.append(sortedMerchant[1][0][1])

        if len(merchant) > 5:
            sortedMerchant = sorted(merchant_prob.iteritems(), key=lambda d: d[1], reverse=True)[0:2]
            for key in sortedMerchant:
                merchant.append(key[0][1])

        stringlist = ''
        for key in merchant:
            stringlist = stringlist + key[0][1] + ':'
        merchants = stringlist[0:len(stringlist) - 1]
        result.append(merchants)
        write1.writerow(result)

writefile1.close()
print "writer the result over ..."
print time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))



