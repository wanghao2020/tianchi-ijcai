from feature_extract import featureExtract
import pickle
ft = featureExtract()
feature = []
label = []
location_merchant = {}

train_path = 'E:\IJCAI_competition\datasets\datasets\ijcai2016_koubei_train'
# ft.get_user_feature(train_path,7,10)
# ft.get_merchant_feature()
# ft.get_UM_feature()

merchant_path = 'E:\IJCAI_competition\datasets\datasets\ijcai2016_merchant_info'
with open(merchant_path) as f:
    for line in f:
        line = line.strip('\r\n')
        merchant,budget,locations = line.split(',')
        location = locations.split(':')
        for loc in location:
            if not location_merchant.has_key(loc):
                location_merchant[loc] = []
            location_merchant[loc].append(merchant)

UML_pair = []
UML_pair_set = set()
UL_set = set()
# default_use_feature = [-1] * 55
# default_merchant_feature = [-1] *53
#default_UM_feature = [-1]* 50 #?
print "merge feature..."
count = 1
with open(train_path) as f:
    for line in f:
        print "count:",count
        count += 1
        line = line.strip('\r\n')
        user,merchant,location,time = line.split(',')
        if (user,location) not in UL_set:
            UL_set.add((user,location))
            for mer in location_merchant[location]:
                feature_list = []
                if (user,mer,location) not in UML_pair_set:
                    UML_pair.append((user,mer,location))
                    UML_pair_set.add((user,mer,location))
                    # if ft.user_feature.has_key(user):
                    #     feature_list.extend(ft.user_feature[user])
                    # else:
                    #     feature_list.extend(default_use_feature)
                    # if ft.merchant_feature.has_key((location,mer)):
                    #     feature_list.extend(ft.merchant_feature[(location,mer)])
                    # else:
                    #     feature_list.extend(default_merchant_feature)
                    # if ft.UM_feature.has_key((user,mer,location)):
                    #     feature_list.extend(ft.UM_feature[(user,mer,location)])
                    # else:
                    #     feature_list.extend(default_UM_feature)
                    # feature.append(feature_list)
print "UML_pair num :",len(UML_pair)

labelpath = 'E:\IJCAI_competition\datasets\datasets\\trainfrom20151101to20151131'
print "get label list..."
label_set = set()
count = 1
with open(labelpath) as f:
    print "count:",count
    count += 1
    for line in f:
        line = line.strip('\r\n')
        user,merchant,location,time = line.split(',')
        if (user,merchant,location) not in label_set:
            label_set.add((user,merchant,location))

positive_num = 0
negative_num = 0
print "get label..."
count  = 1
for pair in UML_pair:
    print "label count:" , count
    count += 1
    if pair in label_set:
        label.append(1)
        positive_num += 1
    else:
        label.append(0)
        negative_num += 1

print "positive label num :",positive_num
print "negative label num :",negative_num

#outfile1 = open('/home/wanghao/Document/tianchi/trainset/feature_from7to10.pkl','wb')
#outfile2 = open('/home/wanghao/Document/tianchi/trainset/label_11.pkl','wb')
#pickle.dump(feature,outfile1)
#pickle.dump(label,outfile2)





