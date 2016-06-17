# coding=utf-8
import koubei_merchant_feature
import koubei_user_feature
import koubei_user_merchant_feature
import taobao_user_feature
import numpy as np
import sys
import csv


class merge_testfeaure():

    test_feature = np.zeros((21320673, 332))
    test_UMLpair = []

    def gettestFeature(self, enddays):

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

        default_koubei_use_feature = [-1] * 53
        default_koubei_merchant_feature = [-1] * 80
        default_koubei_userandmerchant_feature = [-1] * 49
        default_taobao_user_feature = [-1] * 150

        location_merchant = {}
        test_path = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_koubei_test'
        merchant_path = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_merchant_info'

        UML_pair_set = set()
        UL_set = set()

        print "get the location merchants ......"

        with open(merchant_path) as f:
            for line in f:
                line = line.strip('\r\n')
                merchant, budget, locations = line.split(',')
                location = locations.split(':')
                for loc in location:
                    if not location_merchant.has_key(loc):
                        location_merchant[loc] = []
                    location_merchant[loc].append(merchant)

        print "\r\nmerge test data feature......"

        count = 0
        index = 0
        with open(test_path) as f:
            for line in f:
                sys.stdout.write('\rtest feature count %d' % count)
                sys.stdout.flush()
                count += 1

                line = line.strip('\r\n')
                user, location = line.split(',')

                if (user, location) not in UL_set:
                    UL_set.add((user, location))
                    for mer in location_merchant[location]:
                        feature_list = []
                        if (user, mer, location) not in UML_pair_set:

                            self.test_UMLpair.append((user, mer, location))
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

                            if koubeiuserAndmerchantfeature.has_key((user, mer, location)):
                                feature_list.extend(koubeiuserAndmerchantfeature[(user, mer, location)])
                            else:
                                feature_list.extend(default_koubei_userandmerchant_feature)

                            featureArray = np.asarray(feature_list)
                            self.test_feature[index, :] = featureArray
                            index += 1

        print "\r\nUML_pair num :", len(self.test_UMLpair)


if __name__ == '__main__':

    testfeature = merge_testfeaure()
    testfeature.gettestFeature(153)

    print "test feature size is ..."
    print testfeature.test_feature.shape
    print "write the test feature to file"
    np.save('./testfeature.npy', testfeature.test_feature)

    print '*'*50
    print 'write the test pair to file'

    wfile = open('./testpair', 'wb')
    writer = csv.writer(wfile)
    writer.writerows(testfeature.test_UMLpair)
    wfile.close()
