from feature_extract import featureExtract
import pickle
import sys
import numpy as np
# ********************************************
# merge the train data and label by the koubei train file
class mergetestfeature():


    #test_feature = []
    #test_UMLpair = []
    test_feature = np.zeros((21320673,338))
    # test_feature = np.zeros((2132067, 146))
    test_UMLpair = []

    def getTomergetestdata(self):

        ft = featureExtract()
        ft.get_user_feature('/home/wanghao/Document/tianchi/dataset/trainfrom7to11', 7, 11)
        ft.MergeMerchantFeature(7, 11)
        ft.mergeUserMerchantFeature(7, 11)
        ft.get_user_taobao_feature(7,11)

        location_merchant = {}

        test_path = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_koubei_test'
        merchant_path = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_merchant_info'

        UML_pair_set = set()
        UL_set = set()
        default_use_feature = [-1] * 55
        default_merchant_feature = [-1] * 53
        default_userandmerchant_feature = [-1] * 38
        default_user_taobao_feature = [-1] * 192

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

                            if ft.user_feature.has_key(user):
                                feature_list.extend(ft.user_feature[user])
                            else:
                                feature_list.extend(default_use_feature)

                            if ft.user_taobao_feature.has_key(user):
                                feature_list.extend(ft.user_taobao_feature[user])
                            else:
                                feature_list.extend(default_user_taobao_feature)

                            if ft.merchant_feature.has_key((mer, location)):
                                feature_list.extend(ft.merchant_feature[(mer, location)])
                            else:
                                feature_list.extend(default_merchant_feature)

                            if ft.userandmerchant_feature.has_key((user, mer, location)):
                                feature_list.extend(ft.userandmerchant_feature[(user, mer, location)])
                            else:
                                feature_list.extend(default_userandmerchant_feature)

                            featureArray = np.asarray(feature_list)
                            self.test_feature[index,:] = featureArray
                            index += 1

        print "\r\nUML_pair num :", len(self.test_UMLpair)

if __name__ == '__main__':
    # test = mergetestfeature()
    # test.getTomergetraindata()
    # feature = test.test_feature
    # pair = test.test_UMLpair

    # test = mergetestfeature()
    # print "test feature size : ", test.test_feature.shape
    # print test.test_feature[0],len(test.test_feature[0])

    test = mergetestfeature()
    test.getTomergetestdata()
    print "test feature..."
    print test.test_feature.shape
    print "write the test feature to file"
    np.save('./testfeature.npy',test.test_feature)
    print 'write the test pair to file'
    import csv
    wfile = open('./testpair','wb')
    writer = csv.writer(wfile)
    writer.writerows(test.test_UMLpair)
    wfile.close()
