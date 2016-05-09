import math
import csv
# item base CF :
class ItemCF:

    UserMerchantRateMatrix = {}
    itemSimilarityMatrix = {}
    Location_merchant_users = {}
    Location_merchant_nums = {}
    trainuser = 0
    recommendationCount = 0

    # load the user merchant rate matrix
    def readData(self,file):

        with open(file,'rb') as f:
            for line in f:
                user,merchant,location,time = line.split(',')
                if not self.UserMerchantRateMatrix.has_key(user):
                    self.UserMerchantRateMatrix[user] = {}
                if not self.UserMerchantRateMatrix[user].has_key(merchant):
                    self.UserMerchantRateMatrix[user][merchant] = 0
                self.UserMerchantRateMatrix[user][merchant] = self.UserMerchantRateMatrix[user][merchant] + 1

        return self.UserMerchantRateMatrix

    # get the location { merchant  : people nums  }
    def getLocation_merchant_nums(self, trainfile, merchantfile):

        with open(trainfile, 'rb') as f:

            # get the {  location: {merchant ; [user1, user2,...userN]} }
            for line in f:
                user, merchant, location, time = line.split(',')
                if not self.Location_merchant_users.has_key(location):
                    self.Location_merchant_users[location] = {}
                if not self.Location_merchant_users[location].has_key(merchant):
                    self.Location_merchant_users[location][merchant] = []
                if user not in self.Location_merchant_users[location][merchant]:
                    self.Location_merchant_users[location][merchant].append(user)

         # get the location { merchant : nums }
        for location, merchant_users in self.Location_merchant_users.items():

            if not self.Location_merchant_nums.has_key(location):
                self.Location_merchant_nums[location] = {}

            for merchant, users in merchant_users.items():
                nums = len(users)
                self.Location_merchant_nums[location][merchant] = nums



        # involve the merchant info
        with open(merchantfile, 'rb') as f :
            for line in f :
                merchant, budget, locationlists = line.split(',')
                locationlists = locationlists[0:len(locationlists)-1]
                for location in locationlists.split(':'):
                    if not self.Location_merchant_nums.has_key(location):
                        self.Location_merchant_nums[location] = {}
                    if not self.Location_merchant_nums[location].has_key(merchant):
                        self.Location_merchant_nums[location][merchant] = 0

        return self.Location_merchant_nums

    # compute the item similarity matrix
    def itemSimilarity(self):

        C = {}
        N = {}
        for user, items in self.UserMerchantRateMatrix.items():
            for i in items.keys():
                if not N.has_key(i):
                    N[i] = 0
                N[i] = N[i] + 1
                if not C.has_key(i):
                    C[i] = {}
                for j in items.keys():
                    if i == j :
                        continue
                    if not C[i].has_key(j):
                        C[i][j] = 0
                    C[i][j] = C[i][j] + 1

        # compute similarity matrix
        self.itemSimilarityMatrix = {}
        for i,related_item  in C.items():
            if not self.itemSimilarityMatrix.has_key(i):
                self.itemSimilarityMatrix[i] = {}

            for j,cij in related_item.items() :
                self.itemSimilarityMatrix[i][j] = cij / math.sqrt(N[i] * N[j])

        return self.itemSimilarityMatrix


    # get the user score of the one merchant
    def useritemScore(self,user,merchant,k=20):

        user_merchant = self.UserMerchantRateMatrix[user]
        userMerchantSet = set(user_merchant.keys())
        score = -1

        itemsimilarityMerchant = set()

        if len(self.itemSimilarityMatrix[merchant]) < k:
            for m in self.itemSimilarityMatrix[merchant]:
                itemsimilarityMerchant.add(m)
        else:
            sortedsimilarityMerchant = sorted(self.itemSimilarityMatrix[merchant].iteritems(),key=lambda d:d[1],reverse=True)[0:k]
            for m in sortedsimilarityMerchant:
                itemsimilarityMerchant.add(m)

        unionMerchant = userMerchantSet & itemsimilarityMerchant
        for m in unionMerchant :
            score  = score + self.UserMerchantRateMatrix[user][m] * self.itemSimilarityMatrix[m][merchant]

        return score

    def userLocationRecommenation(self,user,location):


        resultMerchant = []
        locationMerchantList = self.Location_merchant_nums[location].keys()
        merchantScore = {}

        if not self.UserMerchantRateMatrix.has_key(user):

            if len(self.Location_merchant_nums[location]) < 4 :
                for m in self.Location_merchant_nums[location]:
                    if self.Location_merchant_nums[location][m] > 0:
                        resultMerchant.append(m)
                return resultMerchant
            else:
                sortedMerchant = sorted(self.Location_merchant_nums[location].iteritems(), key=lambda d: d[1],reverse=True)[0:4]
                for m in sortedMerchant:
                    resultMerchant.append(m[0])
                return resultMerchant
        else:
            self.trainuser = self.trainuser + 1
            for merchant in locationMerchantList :
                score  = self.useritemScore(user,merchant)
                if  score > 0 :
                    merchantScore[merchant] = score

            if len(merchantScore) > 10 :
                sortedMerchant = sorted(merchantScore.iteritems(),key=lambda d:d[1],reverse=True)[0:10]
                for m in sortedMerchant:
                    resultMerchant.append(m[0])
                return resultMerchant

            # top 4
            if len(merchantScore) == 0:
                if len(self.Location_merchant_nums[location]) < 4:
                    for m in self.Location_merchant_nums[location]:
                        if self.Location_merchant_nums[location][m] > 0:
                            resultMerchant.append(m)
                    return resultMerchant
                else:
                    sortedMerchant = sorted(self.Location_merchant_nums[location].iteritems(), key=lambda d: d[1],reverse=True)[0:4]
                    for m in sortedMerchant:
                        resultMerchant.append(m[0])
                    return resultMerchant

            for m in merchantScore:
                resultMerchant.append(m)

            self.recommendationCount = self.recommendationCount + 1


        return resultMerchant


if __name__ == '__main__':

    trainfile = '/home/wanghao/Document/tianchi/data_sets/ijcai2016_koubei_train'
    testfile = '/home/wanghao/Document/tianchi/data_sets/ijcai2016_koubei_test'
    merchantfile = '/home/wanghao/Document/tianchi/data_sets/ijcai2016_merchant_info'

    resultfile = '/home/wanghao/Document/tianchi/result/itemresult.csv'
    itemCf = ItemCF()
    Usermerchant = itemCf.readData(trainfile)
    similarityMatrix = itemCf.itemSimilarity()

    location_merchant_nums = itemCf.getLocation_merchant_nums(trainfile, merchantfile)

    allResult = []
    count = 0
    with open(testfile, 'rb') as f :
        for line in f :
            result = []
            user,location = line.split(',')
            location = location[0 : len(location) -1 ]
            result.append(user)
            result.append(location)
            recommend = itemCf.userLocationRecommenation(user, location)
            string = ''
            for m in recommend:
                string = string + m + ":"
            string = string[0:len(string)-1]
            result.append(string)
            allResult.append(result)

            count = count + 1
            print result

    with open(resultfile,'wb') as f:
        writer = csv.writer(f)
        writer.writerows(allResult)

    print "the user of the train data set num is " , itemCf.trainuser
    print "the num of the recommendation of merchant is : " , itemCf.recommendationCount
    print "the num of the test data is :" , count
    print "Main function"



