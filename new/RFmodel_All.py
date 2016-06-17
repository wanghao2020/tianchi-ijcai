#coding=utf-8

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
from mergeTestFeature import mergetestfeature
from sklearn.externals import joblib
import sys
import csv
import numpy as np
import time
# -------------- get the new model

# get the train data , and label
TrainFeature = np.load('./trainfeature.npy')
TrainLabel = np.load('./trainlabel.npy')

# choose the model
print '*'*50

# --------- Random Forest
print "Train the data by Random Forest model "
RFmodel = RandomForestClassifier(n_estimators=200,criterion='gini',verbose=1,n_jobs=12)
RFmodel.fit(TrainFeature, TrainLabel)

trainPredLabel = RFmodel.predict(TrainFeature)
accy = accuracy_score(TrainLabel, trainPredLabel)
print "The train data by RF accuracy is ", accy

print '*' * 50
print 'save the model ...'
joblib.dump(RFmodel, './copymodel/rf_all/RFmodel.pkl')

# get the test feature
print '*' * 50
print 'Get the test data Feature....'
testdata = np.load('./testfeatue.npy')
print "test data shape", testdata.shape

UMLpairfile = '/home/wanghao/newmodel/testpair'
testUMLpair = []

with open(UMLpairfile, 'rb') as f :
    for line in f :
        line = line.strip('\r\n')
        user,merchant,location = line.split(',')
        testUMLpair.append((user,merchant,location))

RFresult = {}
RFPredictlabel = RFmodel.predict_proba(testdata)
for i in range(len(RFPredictlabel)):
    RFresult[testUMLpair[i]] = RFPredictlabel[i][1]

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

testfile = '/home/wanghao/newmodel/dataset/ijcai2016_koubei_test'
resultfile = '/home/wanghao/model/result/RFresult_prediction.csv'
writefile1 = open(resultfile, 'wb')
write1 = csv.writer(writefile1)
threshold = 0.35
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
            merchant_prob[(user,merchant,location)] = RFresult[(user,merchant,location)]

        sortedMerchant = sorted(merchant_prob.iteritems(), key=lambda d: d[1], reverse=True)
        stringlist = ''
        for key in sortedMerchant:
            stringlist = stringlist + key[0][1] + ':' + key[1] +' , '
        merchants = stringlist[0:len(stringlist) - 1]
        result.append(merchants)
        write1.writerow(result)

writefile1.close()
print "writer the result over ..."
print time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))














