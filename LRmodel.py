#coding=utf-8

from sampling import sampling
from mergeTestFeature import mergetestfeature
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
import sys
import csv
import numpy as np
from merge_traindata import mergetraindata

# -------------- get the new model

# get the train data and label ---------------------
#traindata = mergetraindata()
#traindata.getTomergetraindata()

#trainFeature = np.asarray(traindata.train_feature)
#trainLabel = np.asarray(traindata.train_label)
#trainUMLpair = traindata.train_UMLpair
#print "Train feature size",trainFeature.shape
sam = sampling()
sam.getsampledata()

trainFeature = np.asarray(sam.sampleFeature)
trainLabel = np.asarray(sam.sampleLabel)
trainUMLpair = sam.sampleUML
print "Train feature size",trainFeature.shape

#  Preprocessing-------------------
#scalaTrainFeature = preprocessing.scale(trainFeature)
maxmin_scaler = preprocessing.MinMaxScaler()
scalaTrainFeature = maxmin_scaler.fit_transform(trainFeature)

# choose the model
print '*'*50

# --------- LR model
print "Train the data by LR model "


# 调参数
C = []
threshold = 0.8

LRmodel = LogisticRegression(C=1,penalty='l1',tol=0.001,max_iter=20000)
LRmodel.fit(scalaTrainFeature, trainLabel)

print '*'*50

# get the test feature and UML pair -----------------
print '*' * 50
print 'Get the test data Feature....'
scaleTestFeature = np.load('./testfeature.npy')
print "test feature size",scaleTestFeature.shape

filepair = '/home/wanghao/model/testpair.pkl'
testUMLpair = [] 
with open(filepair,'rb') as f :
    for line in f :
        line = line.strip('\r\n')
        user,merchant,location = line.split(',')
        testUMLpair.append((user,merchant,location))

print 'Processing ....'
#scaleTestFeature = preprocessing.scale(testfeature)
print "predict the test label ..."
testprob = LRmodel.predict_proba(scaleTestFeature)


LRresult = {}
for i in range(len(testprob)):
    LRresult[testUMLpair[i]] = testprob[i]

print "Predict the test label over ..."

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


# get the location : {merchants : nums }
Location_merchant_users = {}
Location_merchant_nums = {}

with open('/home/wanghao/model/dataset/trainfrom7to11', 'rb') as f:

    # get the {  location: {merchant ; [user1, user2,...userN]} }
    for line in f:
        user, merchant, location, time = line.split(',')
        if not Location_merchant_users.has_key(location):
            Location_merchant_users[location] = {}
        if not Location_merchant_users[location].has_key(merchant):
            Location_merchant_users[location][merchant] = []
        if user not in Location_merchant_users[location][merchant]:
            Location_merchant_users[location][merchant].append(user)

            # get the location { merchant : nums }
for location, merchant_users in Location_merchant_users.items():

    if not Location_merchant_nums.has_key(location):
        Location_merchant_nums[location] = {}

    for merchant, users in merchant_users.items():
        nums = len(users)
        Location_merchant_nums[location][merchant] = nums

# involve the merchant info
with open('/home/wanghao/model/ijcai2016_merchant_info', 'rb') as f:
    for line in f:
        merchant, budget, locationlists = line.split(',')
        locationlists = locationlists[0:len(locationlists) - 1]
        for location in locationlists.split(':'):
            if not Location_merchant_nums.has_key(location):
                Location_merchant_nums[location] = {}
            if not Location_merchant_nums[location].has_key(merchant):
                Location_merchant_nums[location][merchant] = 0



# Get the test label and write to the file

testfile = '/home/wanghao/model/ijcai2016_koubei_test'


LRtest = []
with open(testfile, 'rb') as f:
    count = 0
    for line in f :
        count += 1
        sys.stdout.write('\rtest current count %d'%count)
        sys.stdout.flush()

        lrresult = []

        line = line.strip('\r\n')
        user,location = line.split(',')

        lrresult.append(user)
        lrresult.append(location)


        lrmerchant_prob = {}

        for merchant in location_merchants[location]:
            if LRresult[(user,merchant,location)] > threshold:
                lrmerchant_prob[(user,merchant,location)] = LRresult[(user,merchant,location)]

        if len(lrmerchant_prob) > 10 :
            str = ''
            sortedMerchant = sorted(lrmerchant_prob.iteritems(), key=lambda d: d[1],reverse=True)[0:10]
            for key in sortedMerchant:
                str = str + key[0][1] + ':'
            lrmerchants = str[0:len(str) - 1]
            lrresult.append(lrmerchants)
            LRtest.append(lrresult)

        elif len(lrmerchant_prob) == 0 :
            str = ''
            sortedMerchant = sorted(Location_merchant_nums[location].iteritems(), key=lambda d: d[1],reverse=True)[0:3]
            for m in sortedMerchant:
                str = str + m[0] + ':'
            lrmerchants = str[0:len(str) - 1]
            lrresult.append(lrmerchants)
            LRtest.append(lrresult)

        else:
            str = ''
            for key in lrmerchant_prob.keys():
                str = str + key[1] + ':'
            lrmerchants = str[0:len(str) - 1]
            lrresult.append(lrmerchants)
            LRtest.append(lrresult)

lrresultfile = '/home/wanghao/model/result/lrresult.csv'

print "write the result to result file ...."

writefile1 = open(lrresultfile, 'wb')

write1 = csv.writer(writefile1)

write1.writerows(LRtest)











