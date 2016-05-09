import math
import csv


# just recommend the merchant tha user visted
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

    # get the location { merchant  : people nums }
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


    def userLocationRecommenation(self,user,location):


        resultMerchant = []
        locationMerchantList = self.Location_merchant_nums[location].keys()

        if not self.UserMerchantRateMatrix.has_key(user):
            # the train file does not include the user
            if len(self.Location_merchant_nums[location]) < 3 :
                for m in self.Location_merchant_nums[location]:
                    #if self.Location_merchant_nums[location][m] > 0:
                    resultMerchant.append(m)
                return resultMerchant
            else:
                sortedMerchant = sorted(self.Location_merchant_nums[location].iteritems(), key=lambda d: d[1],reverse=True)[0:3]
                for m in sortedMerchant:
                    resultMerchant.append(m[0])
                return resultMerchant
        else:

            userVisitedMerchants = self.UserMerchantRateMatrix[user].keys()
            for m in userVisitedMerchants :
                if self.Location_merchant_nums[location].has_key(m):
                    resultMerchant.append(m)

            if len(resultMerchant) == 0:
                if len(self.Location_merchant_nums[location]) < 3:
                    for m in self.Location_merchant_nums[location]:
                        if self.Location_merchant_nums[location][m] > 0:
                            resultMerchant.append(m)
                    return resultMerchant
                else:
                    sortedMerchant = sorted(self.Location_merchant_nums[location].iteritems(), key=lambda d: d[1],reverse=True)[0:3]
                    for m in sortedMerchant:
                        resultMerchant.append(m[0])
                    return resultMerchant

            self.recommendationCount = self.recommendationCount + 1
            return resultMerchant


if __name__ == '__main__':

    trainfile = '/home/wanghao/Document/tianchi/data_sets/ijcai2016_koubei_train'
    testfile = '/home/wanghao/Document/tianchi/data_sets/ijcai2016_koubei_test'
    merchantfile = '/home/wanghao/Document/tianchi/data_sets/ijcai2016_merchant_info'

    resultfile = '/home/wanghao/Document/tianchi/result/visitedresult6.csv'
    itemCf = ItemCF()
    Usermerchant = itemCf.readData(trainfile)

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



