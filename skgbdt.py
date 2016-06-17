from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import  train_test_split
import numpy as np
import time
import sys
import csv

traindata = np.load('./samplefeature.npy')
trainlabel = np.load('./samplelabel.npy')

X_train,X_validation,Y_train,Y_validation = train_test_split(traindata,trainlabel,test_size=0.2,random_state=0)

print "get data over ..."
print time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))
clf = GradientBoostingClassifier(n_estimators=100, learning_rate=0.5,max_depth=3, random_state=0,verbose=1)
clf.fit(X_train, Y_train)

print 'train data over ...'
print time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))

print "gbdt train result... ", clf.score(X_validation,Y_validation)
print time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))


print "the test ..."
testdata = np.load('./testfeatue.npy')
print "test data shape", testdata.shape

UMLpairfile = '/home/wanghao/model/testpair'
testUMLpair = []

with open(UMLpairfile, 'rb') as f :
    for line in f :
        line = line.strip('\r\n')
        user,merchant,location = line.split(',')
        testUMLpair.append((user,merchant,location))

GBDTresult = {}
y_pred = clf.predict_proba(testdata)
for i in range(len(y_pred)):
    GBDTresult[testUMLpair[i]] = y_pred[i][1]

print "Predict the test label over ..."
print time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))

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
resultfile = '/home/wanghao/model/result/skGBDTresult.csv'
writefile1 = open(resultfile, 'wb')
write1 = csv.writer(writefile1)

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
            merchant_prob[(user,merchant,location)] = GBDTresult[(user,merchant,location)]

        sortedMerchant = sorted(merchant_prob.iteritems(), key=lambda d: d[1],reverse=True)[0:4]
        str = ''
        for key in sortedMerchant:
            str = str + key[0][1] + ':'
        merchants = str[0:len(str) - 1]
        result.append(merchants)
        write1.writerow(result)

writefile1.close()
print "writer the result over ..."
print time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))




