import xgboost as xgb
import numpy as np
from merge_traindata import mergetraindata
from sklearn.cross_validation import train_test_split
from sampling import sampling
import sys
import csv


''''
Xgboost ... can not use
'''''
# traindata = mergetraindata()
# traindata.getTomergetraindata()
# trainFeature = mergetraindata.train_feature
# trainLabel = mergetraindata.train_label
# trainUML = mergetraindata.train_UMLpair

# trainFeature = sam.sampleFeature
# trainLabel = sam.sampleLabel
# trainUMLpair = sam.sampleUML
#
# trainFeatureArray = np.asarray(trainFeature)
# trainLabelArray = np.asarray(trainLabel)

trainFeatureArray = np.load('./samplefeature1to10.npy')
trainLabelArray = np.load('./samplelabel1to10.npy')

X_train,X_validation,Y_train,Y_validation = train_test_split(trainFeatureArray,trainLabelArray,test_size=0.2,random_state=0)


print "get the train data and validation data ..."
dtrain = xgb.DMatrix(data=X_train, label=Y_train)
dvalidation = xgb.DMatrix(data=X_validation, label=Y_validation)
param = {'max_depth':5, 'eta':0.3, 'silent':1,'objective':'binary:logistic'}
watchlist = [(dvalidation,'eval'),(dtrain, 'train')]
num_round = 30
print "train the model ..."
bst = xgb.train(param,dtrain,num_round,watchlist)

print 'predict the model ...'
GBDTresult = {}


print "get the test data  ..."
testFeatureArray = np.load('./testfeature.npy')
dtest = xgb.DMatrix(testFeatureArray)
ypred = bst.predict(dtest)

UMLpairfile = '/home/wanghao/newmodel/testpair'
testUMLpair = []
with open(UMLpairfile, 'rb') as f :
    for line in f :
        line = line.strip('\r\n')
        user,merchant,location = line.split(',')
        testUMLpair.append((user,merchant,location))

for i in range(len(ypred)):
    GBDTresult[testUMLpair[i]] = ypred[i]


print "Predict the test label over ..."

# get the location_ merchants data
merchantinfo = '/home/wanghao/newmodel/dataset/ijcai2016_merchant_info'
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


# # get the location : {merchants : nums }
# Location_merchant_users = {}
# Location_merchant_nums = {}
#
# with open('/home/wanghao/model/dataset/trainfrom7to11', 'rb') as f:
#
#     # get the {  location: {merchant ; [user1, user2,...userN]} }
#     for line in f:
#         user, merchant, location, time = line.split(',')
#         if not Location_merchant_users.has_key(location):
#             Location_merchant_users[location] = {}
#         if not Location_merchant_users[location].has_key(merchant):
#             Location_merchant_users[location][merchant] = []
#         if user not in Location_merchant_users[location][merchant]:
#             Location_merchant_users[location][merchant].append(user)
#
#             # get the location { merchant : nums }
# for location, merchant_users in Location_merchant_users.items():
#
#     if not Location_merchant_nums.has_key(location):
#         Location_merchant_nums[location] = {}
#
#     for merchant, users in merchant_users.items():
#         nums = len(users)
#         Location_merchant_nums[location][merchant] = nums
#
# # involve the merchant info
# with open('/home/wanghao/model/ijcai2016_merchant_info', 'rb') as f:
#     for line in f:
#         merchant, budget, locationlists = line.split(',')
#         locationlists = locationlists[0:len(locationlists) - 1]
#         for location in locationlists.split(':'):
#             if not Location_merchant_nums.has_key(location):
#                 Location_merchant_nums[location] = {}
#             if not Location_merchant_nums[location].has_key(merchant):
#                 Location_merchant_nums[location][merchant] = 0


# Get the test label and write to the file

testfile = '/home/wanghao/newmodel/dataset/ijcai2016_koubei_test'

threshold = 0.6
GBDTtest = []
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
            if GBDTresult[(user,merchant,location)] > threshold:
                merchant_prob[(user,merchant,location)] = GBDTresult[(user,merchant,location)]

        sortedMerchant = sorted(merchant_prob.iteritems(), key=lambda d: d[1], reverse=True)
        stringlist = ''
        for key in sortedMerchant:
            stringlist = stringlist + key[0][1] + ':' + key[1] + ' , '
        merchants = stringlist[0:len(stringlist) - 1]
        result.append(merchants)
        GBDTtest.append(result)

lrresultfile = '/home/wanghao/newmodel/result/GBDTresult.csv'

print "write the result to result file ...."

writefile1 = open(lrresultfile, 'wb')

write1 = csv.writer(writefile1)

write1.writerows(GBDTtest)




