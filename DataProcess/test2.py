from GetFeature import feature
import pickle

if __name__ == '__main__':

    feature_path = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_koubei_train'

    ft = feature()
    ft.get_location_merchant_feature(feature_path)
    ft.get_user_feature(feature_path)
    ft.get_user_merchant_feature(feature_path)

    sample = []
    UML_pair = []
    count = 1

    featureList = {}
    print "-" * 50
    print "generate the feature vector ..."
    with open(feature_path) as f:
        for line in f:
            print count
            count += 1
            user, merchant, location, time = line.split(',')
            if (user, merchant, location) not in UML_pair:
                UML_pair.append((user, merchant, location))
                sam = []
                sam.extend(ft.merchant_feature[(location, merchant)])
                sam.extend(ft.user_feature[user])
                sam.extend(ft.UM_feature[(user, merchant, location)])

                if not featureList.has_key((user,merchant,location)):
                    featureList[(user, merchant, location)] = sam

    print "get feature done!"
    outfile = open('/home/wanghao/Document/tianchi/testset/featureall.pkl', 'wb')
    pickle.dump(featureList, outfile)
    outfile.close()
