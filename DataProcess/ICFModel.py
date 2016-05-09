import math
import numpy as np

# based on the item recommendation
# author : Hao

def MerchantSim(merchantA, merchantB):

    usersetA = set(merchantA.keys())
    usersetB = set(merchantB.keys())
    commonuserset = usersetA & usersetB

    # similarity
    upperValue = 0.0
    for user in commonuserset:
        upperValue  = upperValue + merchantA[user] * merchantB[user]

    partA = 0.0
    for user in merchantA.keys():
        partA = partA + merchantA[user] * merchantA[user]

    partB = 0.0
    for user in merchantB.keys():
        partB = partB + merchantB[user] * merchantB[user]

    return upperValue / (math.sqrt(partA) * math.sqrt(partB))

def getMerchantUser(file):

    result_dict = {}
    with open(file,'rb') as f :
        for line in f:
            linelists = line.split(',')
            user = linelists[0]
            merchant = linelists[1]
            if result_dict.has_key(merchant):
                if result_dict[merchant].has_key(user):
                    result_dict[merchant][user] = result_dict[merchant][user] + 1
                else:
                    result_dict[merchant][user] = 1
            else:
                merchantitem = {}
                merchantitem[user] = 1
                result_dict[merchant] = merchantitem

    return result_dict

def changMerchantIdtoIndex(file):

    merchant_index = {}
    index = 0
    with open(file,'rb') as f :
        for line in f :
            linelists = line.split(',')
            merchant = linelists[1]
            if not merchant_index.has_key(merchant):
                merchant_index[merchant] = index
                index  = index + 1

    return merchant_index



def getMerchantsSimilarityMatrix(file):

    print "Get the similaritity matrix between merchant"

    merchant_index = changMerchantIdtoIndex(file)
    merchants = merchant_index.keys()
    merchant_users = getMerchantUser(file)

    merchantSimilarityMatrix = np.zeros((len(merchants),len(merchants)))

    count = 1
    for merchantA in merchants:
        print count
        for merchantB in merchants:
            sim = MerchantSim(merchant_users[merchantA],merchant_users[merchantB])
            merchantSimilarityMatrix[merchant_index[merchantA],merchant_index[merchantB]] = sim
        count = count + 1

    return merchantSimilarityMatrix






if __name__ == '__main__':

    file = '/home/wanghao/Document/tianchi/data_sets/ijcai2016_koubei_train'
    simi =  getMerchantsSimilarityMatrix(file)

    merchant_index = changMerchantIdtoIndex(file)

    ##




