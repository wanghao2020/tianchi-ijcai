#
# #coding=utf-8
# import math
# import csv
#
#
# # just recommend the merchant tha user visted
# class ItemCF:
#
#     UserMerchantRateMatrix = {}
#     itemSimilarityMatrix = {}
#     Location_merchant_users = {}
#     Location_merchant_nums = {}
#     trainuser = 0
#     recommendationCount = 0
#     location_merchant_users11 = {}
#
#     # load the user merchant rate matrix
#     def readData(self,file):
#
#         with open(file,'rb') as f:
#             for line in f:
#                 user,merchant,location,time = line.split(',')
#                 if not self.UserMerchantRateMatrix.has_key(user):
#                     self.UserMerchantRateMatrix[user] = {}
#                 if not self.UserMerchantRateMatrix[user].has_key(merchant):
#                     self.UserMerchantRateMatrix[user][merchant] = 0
#                 self.UserMerchantRateMatrix[user][merchant] = self.UserMerchantRateMatrix[user][merchant] + 1
#
#         return self.UserMerchantRateMatrix
#
#     # get the location { merchant  : people nums }
#     def getLocation_merchant_nums(self, trainfile, merchantfile):
#
#         with open(trainfile, 'rb') as f:
#
#             # get the {  location: {merchant ; [user1, user2,...userN]} }
#             for line in f:
#                 user, merchant, location, time = line.split(',')
#                 if not self.Location_merchant_users.has_key(location):
#                     self.Location_merchant_users[location] = {}
#                 if not self.Location_merchant_users[location].has_key(merchant):
#                     self.Location_merchant_users[location][merchant] = []
#                 if user not in self.Location_merchant_users[location][merchant]:
#                     self.Location_merchant_users[location][merchant].append(user)
#
#          # get the location { merchant : nums }
#         for location, merchant_users in self.Location_merchant_users.items():
#
#             if not self.Location_merchant_nums.has_key(location):
#                 self.Location_merchant_nums[location] = {}
#
#             for merchant, users in merchant_users.items():
#                 nums = len(users)
#                 self.Location_merchant_nums[location][merchant] = nums
#
#
#
#         # involve the merchant info
#         with open(merchantfile, 'rb') as f :
#             for line in f :
#                 merchant, budget, locationlists = line.split(',')
#                 locationlists = locationlists[0:len(locationlists)-1]
#                 for location in locationlists.split(':'):
#                     if not self.Location_merchant_nums.has_key(location):
#                         self.Location_merchant_nums[location] = {}
#                     if not self.Location_merchant_nums[location].has_key(merchant):
#                         self.Location_merchant_nums[location][merchant] = 0
#
#         return self.Location_merchant_nums
#
#     # 统计在11月份最热门的商家
#     def get11location_merchant_users(self):
#
#         file = '/home/wanghao/Document/tianchi/dataset/train11'
#         with open(file, 'rb') as f :
#             for line in f :
#                 line = line.strip('\r\n')
#                 user,merchant,location,time = line.split(',')
#                 if not self.location_merchant_users11.has_key(location):
#                     self.location_merchant_users11[location] = {}
#                 if not self.location_merchant_users11[location].has_key(merchant):
#                     self.location_merchant_users11[location][merchant] = 0
#
#                 self.location_merchant_users11[location][merchant] += 1
#
#     # 用户在这个地点的推荐
#     def userLocationRecommenation(self,user,location):
#
#
#         resultMerchant = []
#
#         if not self.UserMerchantRateMatrix.has_key(user):
#             # the train file does not include the user
#             if not self.location_merchant_users11.has_key(location):
#                 sortedMerchant = sorted(self.Location_merchant_nums[location].iteritems(), key=lambda d: d[1],
#                                         reverse=True)[0:3]
#                 for m in sortedMerchant:
#                     resultMerchant.append(m[0])
#                 return resultMerchant
#             else:
#                 sortedMerchant = sorted(self.location_merchant_users11[location].iteritems(), key=lambda d: d[1],reverse=True)[0:3]
#                 for m in sortedMerchant:
#                     resultMerchant.append(m[0])
#                 return resultMerchant
#         else:
#
#             userVisitedMerchants = self.UserMerchantRateMatrix[user].keys()
#             for m in userVisitedMerchants :
#                 if self.Location_merchant_nums[location].has_key(m):
#                     resultMerchant.append(m)
#
#             # top 4
#             if len(resultMerchant) == 0:
#                 if not self.location_merchant_users11.has_key(location):
#                     sortedMerchant = sorted(self.Location_merchant_nums[location].iteritems(), key=lambda d: d[1],
#                                             reverse=True)[0:3]
#                     for m in sortedMerchant:
#                         resultMerchant.append(m[0])
#                     return resultMerchant
#                 else:
#                     sortedMerchant = sorted(self.location_merchant_users11[location].iteritems(), key=lambda d: d[1],
#                                             reverse=True)[0:3]
#                     for m in sortedMerchant:
#                         resultMerchant.append(m[0])
#                     return resultMerchant
#
#             self.recommendationCount = self.recommendationCount + 1
#             return resultMerchant
#
#
# if __name__ == '__main__':
#
#     rffile = '/home/wanghao/Document/tianchi/result/5-21/RFresult3.csv'
#     bestfile = '/home/wanghao/Document/tianchi/result/newvisitedresult.csv'
#     writerfile = open('/home/wanghao/523.csv','wb')
#     import csv
#     writer = csv.writer(writerfile)
#
#     trainfile = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_koubei_train'
#     testfile = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_koubei_test'
#     merchantfile = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_merchant_info'
#
#     itemCf = ItemCF()
#     location_merchant_num = itemCf.getLocation_merchant_nums(trainfile,merchantfile)
#     Usermerchant = itemCf.readData(trainfile)
#
#     itemCf.get11location_merchant_users()
#
#     allResult = []
#     count = 0
#     with open(rffile, 'rb') as f :
#         for line in f :
#             result = []
#             user,location,merchants = line.strip('\r\n').split(',')
#
#             if not itemCf.UserMerchantRateMatrix.has_key(user):
#                 result.append(user)
#                 result.append(location)
#                 result.append(merchants)
#             else:
#                 resultMerchant = []
#                 userVisitedMerchants = itemCf.UserMerchantRateMatrix[user].keys()
#                 for m in userVisitedMerchants:
#                     if itemCf.Location_merchant_nums[location].has_key(m):
#                         resultMerchant.append(m)
#                 if len(resultMerchant) != 0:
#                     result.append(user)
#                     result.append(location)
#                     string = ''
#                     for m in resultMerchant:
#                         string = string + m + ":"
#                     string = string[0:len(string) - 1]
#                     result.append(string)
#                 else:
#                     result.append(user)
#                     result.append(location)
#                     result.append(merchants)
#
#             writer.writerow(result)
#
#
#     writerfile.close()
#
#
#
#
#
