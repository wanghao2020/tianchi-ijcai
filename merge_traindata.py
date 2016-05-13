from feature_extract import featureExtract
import pickle
ft = featureExtract()
feature = []
label = []
location_merchant = {}

train_path = '/home/wanghao/Document/tianchi/trainset/trainfrom20150701to20151031'
ft.get_user_feature(train_path,7,10)
ft.get_merchant_feature()
ft.get_UM_feature()

merchant_path = '/home/wanghao/Document/tianchi/trainset/ijcai2016_merchantinfo'
with open(merchant_path) as f:
    for line in f:
        line = line.strip('\r\n')
        merchant,budget,location = line.split(',')
        if not location_merchant.has_key(location):
            location_merchant[location] = []
        location_merchant[location].append(merchant)

UML_pair = []
default_use_feature = [-1] * 55
default_merchant_feature = [-1] *53
default_UM_feature = [-1]* 50 #?
print "merge feature..."
with open(train_path) as f:
    for line in f:
        line = line.strip('\r\n')
        user,merchant,location,time = line.split(',')
        for mer in location_merchant[location]:
            feature_list = []
            if (user,mer,location) not in UML_pair:
                UML_pair.append((user,mer,location))
                if ft.user_feature.has_key(user):
                    feature_list.extend(ft.user_feature[user])
                else:
                    feature_list.extend(default_use_feature)
                if ft.merchant_feature.has_key((location,mer)):
                    feature_list.extend(ft.merchant_feature[(location,mer)])
                else:
                    feature_list.extend(default_merchant_feature)
                if ft.UM_feature.has_key((user,mer,location)):
                    feature_list.extend(ft.UM_feature[(user,mer,location)])
                else:
                    feature_list.extend(default_UM_feature)
                feature.append(feature_list)

labelpath = '/home/wanghao/Document/tianchi/trainset/trainfrom20151101to20151131'
print "get label list..."
label_list = []
with open(labelpath) as f:
    for line in f:
        line = line.strip('\r\n')
        user,merchant,location,time = line.split(',')
        if (user,merchant,location) not in label_list:
            label_list.append((user,merchant,location))

print "get label..."
for pair in UML_pair:
    if pair in label_list:
        label.append(1)
    else:
        label.append(0)

outfile1 = open('/home/wanghao/Document/tianchi/trainset/feature_from7to10.pkl','wb')
outfile2 = open('/home/wanghao/Document/tianchi/trainset/label_11.pkl','wb')
pickle.dump(feature,outfile1)
pickle.dump(label,outfile2)



