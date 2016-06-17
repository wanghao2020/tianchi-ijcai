import numpy as np
from sklearn.externals import joblib
import csv
import time
import sys

testfeature = np.load('./testfeature.npy')
testpairfile = './testpair'
testpair = []
with open(testpairfile, 'rb') as f :
    for line in f :
        line = line.strip('\r\n')
        user,merchant,location = line.split(',')
        testpair.append((user,merchant,location))

print 'load model ...'
model = joblib.load('/home/wanghao/model/copymodel/gbdt/skgbdt.pkl')
print 'load model over ...'
y_pred = model.predict_proba(testfeature)
testResult = {}
for i in range(len(y_pred)):
    testResult[testpair[i]] = y_pred[i][1]

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

testfile = '/home/wanghao/model/ijcai2016_koubei_test'
resultfile = '/home/wanghao/model/result/gbdtresult0.35'
writefile1 = open(resultfile, 'wb')
write1 = csv.writer(writefile1)

with open(testfile, 'rb') as f:
    count = 0
    for line in f :
        count += 1
        sys.stdout.write('\rtrain current count %d'%count)
        sys.stdout.flush()

        result = []

        line = line.strip('\r\n')
        user,location = line.split(',')

        result.append(user)
        result.append(location)

        merchants = []
        merchant_prob = {}
        for merchant in location_merchants[location]:
            merchant_prob[merchant] = testResult[(user,merchant,location)]
            if testResult[(user,merchant,location)] > 0.35:
                merchants.append(merchant)

        stringlist = ''
        if len(merchants) == 0 :
            sortedMerchant = sorted(merchant_prob.iteritems(), key=lambda d: d[1], reverse=True)[0:2]
            for key in sortedMerchant:
                stringlist = stringlist + key[0][1] + ':'
            stringlist = stringlist[0:len(stringlist) - 1]

        elif len(merchants) > 5:
            sortedMerchant = sorted(merchant_prob.iteritems(), key=lambda d: d[1], reverse=True)[0:5]
            for key in sortedMerchant:
                stringlist = stringlist + key[0][1] + ':'
            stringlist = stringlist[0:len(stringlist) - 1]

        else:
            for mer in merchants:
                stringlist = stringlist + mer + ':'
            stringlist = stringlist[0:len(stringlist)-1]

        result.append(stringlist)
        write1.writerow(result)

writefile1.close()
print "writer the result over ..."
print time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))



