# coding=utf-8
import koubei_merchant_feature
import koubei_user_feature
import koubei_user_merchant_feature
import taobao_user_feature
import numpy as np
import sys
import csv

class traindata():

    train_feature = []
    train_UMLpair = []
    train_label = []
    train_positive_feature = []
    train_positive_UMLpair = []
    train_negative_feature = []
    train_negative_UMLpair = []

    def getTraindata(self, enddays):

        if enddays == 123:
            endmonth = 10
        if enddays == 153:
            endmonth = 11

        kb_user = koubei_user_feature.koubeiUserFeature()
        kb_user.mergeuserFeature(enddays)
        koubeiuserfeature = kb_user.koubei_user_feature
        print '*' * 50


        kb_merchant = koubei_merchant_feature.koubeiMerchantFeature()
        kb_merchant.mergeMerchantFeature(enddays)
        koubeimerchantfeature = kb_merchant.koubei_merchant_feature
        print '*' * 50

        kb_userandmerchant = koubei_user_merchant_feature.koubeiUserMerchantFeature()
        kb_userandmerchant.mergeUserandMerchantFeature(enddays)
        koubeiuserAndmerchantfeature = kb_userandmerchant.UserAndMerchantFeature
        print '*' * 50

        tb_user = taobao_user_feature.taobaoUserFeature()
        tb_user.mergeTaobaoUserFeature(enddays)
        taobaouserfeature = tb_user.taobao_userFeature
        print '*' * 50

        location_merchant = {}

        train_path = '/home/wanghao/Document/tianchi/dataset/train11'
        merchant_path = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_merchant_info'

        UML_pair_set = set()
        UL_set = set()
        default_koubei_use_feature = [-1] * 53
        default_koubei_merchant_feature = [-1] * 80
        default_koubei_userandmerchant_feature = [-1] * 49
        default_taobao_user_feature = [-1] * 150

        print "get the under the of location merchants ......"

        with open(merchant_path) as f:
            for line in f:
                line = line.strip('\r\n')
                merchant, budget, locations = line.split(',')
                location = locations.split(':')
                for loc in location:
                    if not location_merchant.has_key(loc):
                        location_merchant[loc] = []
                    location_merchant[loc].append(merchant)

        print "merge train data feature......"

        count = 1

        with open(train_path) as f:
            for line in f:
                sys.stdout.write('\rtrain feature count %d' % count)
                sys.stdout.flush()
                count += 1

                line = line.strip('\r\n')
                user, merchant, location, time = line.split(',')

                if (user, location) not in UL_set:
                    UL_set.add((user, location))
                    for mer in location_merchant[location]:
                        feature_list = []
                        if (user, mer, location) not in UML_pair_set:
                            UML_pair_set.add((user, mer, location))

                            if koubeiuserfeature.has_key(user):
                                feature_list.extend(koubeiuserfeature[user])
                            else:
                                feature_list.extend(default_koubei_use_feature)

                            if taobaouserfeature.has_key(user):
                                feature_list.extend(taobaouserfeature[user])
                            else:
                                feature_list.extend(default_taobao_user_feature)

                            if koubeimerchantfeature.has_key((mer, location)):
                                feature_list.extend(koubeimerchantfeature[(mer, location)])
                            else:
                                feature_list.extend(default_koubei_merchant_feature)

                            if koubeiuserAndmerchantfeature.has_key((user, mer)):
                                feature_list.extend(koubeiuserAndmerchantfeature[(user, mer)])
                            else:
                                feature_list.extend(default_koubei_userandmerchant_feature)

                            self.train_UMLpair.append((user, mer, location))
                            self.train_feature.append(feature_list)

        print "\r\nUML_pair num :", len(self.train_UMLpair)

        labelpath = '/home/wanghao/Document/tianchi/dataset/train11'
        print "get (user,merchant,location) pairs......."
        label_set = set()
        count = 1
        with open(labelpath) as f:
            for line in f:
                sys.stdout.write("\rfind label count %d" % count)
                sys.stdout.flush()
                count += 1
                line = line.strip('\r\n')
                user, merchant, location, time = line.split(',')
                if (user, merchant, location) not in label_set:
                    label_set.add((user, merchant, location))

        positive_num = 0
        negative_num = 0
        print "\r\nset label..."
        count = 1
        for i in range(len(self.train_UMLpair)):
            sys.stdout.write("\rlabel count : %d" % count)
            sys.stdout.flush()
            count += 1

            if self.train_UMLpair[i] in label_set:
                self.train_label.append(1)
                positive_num += 1
                self.train_positive_feature.append(self.train_feature[i])
                self.train_positive_UMLpair.append(self.train_UMLpair[i])

            else:
                self.train_label.append(0)
                negative_num += 1
                self.train_negative_feature.append(self.train_feature[i])
                self.train_negative_UMLpair.append(self.train_UMLpair[i])

        print "\r\npositive label num :", positive_num
        print "negative label num :", negative_num
        print 'all nums', positive_num + negative_num



if __name__ == '__main__':

    traind = traindata()
    traind.getTraindata(123)
    print 'save the train feature ...'
    trainfeature = np.asarray(traind.train_feature)
    print 'the train feature size is ', trainfeature.shape
    np.save('./trainfeature.npy', trainfeature)

    print '*'*50
    print 'save the train label ...'
    trainlabel = np.asarray(traind.train_label)
    print 'the train label size is ', trainlabel.shape
    np.save('./trainlabel.npy',trainlabel)

    print '*' * 50
    print 'save the train uml ...'
    wfile = open('/home/wanghao/newmodel/trainUML','wb')
    writer = csv.writer(wfile)
    writer.writerows(traind.train_UMLpair)
    wfile.close()

    print ''
    print '*' * 50
    print 'save the positive train feature ....'
    trainpositivefeature = np.asarray(traind.train_positive_feature)
    print 'the train positive feature size is ', trainpositivefeature.shape
    np.save('./trainpositivefeature.npy',trainpositivefeature)

    print '*'*50
    print 'save the positive train uml ...'
    wfile = open('/home/wanghao/newmodel/trainpositiveUML','wb')
    writer = csv.writer(wfile)
    writer.writerows(traind.train_positive_UMLpair)
    wfile.close()

    print ''
    print '*' * 50
    print 'save the negative train feature ....'
    trainnegativefeature = np.asarray(traind.train_negative_feature)
    print 'the train negative feature size is ', trainnegativefeature.shape
    np.save('./trainnegativefeature.npy', trainnegativefeature)

    print '*' * 50
    print 'save the negative train uml ...'
    wfile = open('/home/wanghao/newmodel/trainnegativeUML', 'wb')
    writer = csv.writer(wfile)
    writer.writerows(traind.train_negative_UMLpair)
    wfile.close()






