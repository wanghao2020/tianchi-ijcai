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
from evaluation import evaluation
from merge_traindata import mergetraindata
# -------------- get the new model

# get the train data , and label
#sam = sampling()
#sam.getsampledata()
traindata = mergetraindata()
traindata.getTomergetraindata()


trainFeature = np.asarray(traindata.train_feature)
print "Train feature size",trainFeature.shape
trainLabel = np.asarray(traindata.train_label)
trainUMLpair = traindata.train_UMLpair


#scalaTrainFeature = preprocessing.scale(trainFeature)
maxmin_scaler = preprocessing.MinMaxScaler()
scalaTrainFeature = maxmin_scaler.fit_transform(trainFeature)

# choose the model
print '*'*50

# --------- LR model
print "Train the data by LR model "


# 调参数
C = []
threshold = 0.6

LRmodel = LogisticRegression(C=1,penalty='l1',tol=0.001,max_iter=20000)
LRmodel.fit(scalaTrainFeature, trainLabel)

Yprob = LRmodel.predict_proba(scalaTrainFeature)

UML_predictlabel = {}
for i in range(len(Yprob)):
    if Yprob[i][1] > threshold:
        UML_predictlabel[trainUMLpair[i]] = 1
    else:
        UML_predictlabel[trainUMLpair[i]] = 0

# get the location:merhants
merchantinfo = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_merchant_info'
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

UMLPredict = {}
traintestfile = '/home/wanghao/Document/tianchi/dataset/train11'
allresult = []
ULset = set()
with open(traintestfile, 'rb') as f :
    for line in f :
        line = line.strip('\r\n')
        user,merchant,location,time = line.split(',')
        if (user,location) not in ULset:
            ULset.add((user,location))
            result =  []
            result.append(user)
            result.append(location)
            resultmerchant = [ ]
            for merchant in location_merchants[location]:
                if UML_predictlabel[(user,merchant,location)] == 1:
                    resultmerchant.append(merchant)

            if len(resultmerchant) != 0:
                str = ''
                for mer in resultmerchant:
                    str = str + mer + ':'
                str = str[0:len(str)-1]
                result.append(str)
                allresult.append(result)
outfile = open('/home/wanghao/Document/tianchi/trainset/trainresult.csv','wb')
import csv
writer = csv.writer(outfile)
writer.writerows(outfile)
outfile.close()

# evaluate the result
eval = evaluation()
truefile = '/home/wanghao/Document/tianchi/dataset/train11'
predictfile = '/home/wanghao/Document/tianchi/trainset/trainresult.csv'
merchantfile = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_merchant_info'
eval.getS_true(truefile)
eval.getS_predict(predictfile)
eval.get_MerchantBudget(merchantfile)
f1 = eval.comp_f1_score()

print "This train F1 score is ", f1















