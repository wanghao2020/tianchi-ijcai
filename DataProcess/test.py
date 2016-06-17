import csv
import random

#
# file1 = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_koubei_test'
# file2 = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_merchant_info'
#
# location_merchants = {}
# with open(file2, 'rb') as f:
#     for line in f:
#         line = line.strip('\r\n')
#         merchant, budget, locations = line.split(',')
#         for loc in locations.split(':'):
#             if not location_merchants.has_key(loc):
#                 location_merchants[loc] = []
#             if merchant not in location_merchants[loc]:
#                 location_merchants[loc].append(merchant)
#
# user_merchant_location= set()
# user_location = set()
# count = 0
# with open(file1, 'rb') as f :
#     for line in f :
#         line = line.strip('\r\n')
#         user,location= line.split(',')
#         if (user, location) not in user_location:
#             for m in location_merchants[location]:
#                 user_merchant_location.add((user,m,location))
#             user_location.add((user,location))
#         print count
#         count += 1
#
# print "the size", len(user_merchant_location)


file1 = '/home/wanghao/Document/tianchi/dataset/trainfrom7to10'
file2 = '/home/wanghao/Document/tianchi/dataset/train11'
testfile = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_koubei_test'
user7 = set()
user8 = set()
user9 = set()
user10 = set()
user11 = set()
user12 = set()
with open('/home/wanghao/Document/tianchi/dataset/train7','rb') as f:
    for line in f :
        user,merchant,location,time = line.split(',')
        if user not in user7:
            user7.add(user)

with open('/home/wanghao/Document/tianchi/dataset/train8','rb') as f:
    for line in f :
        user,merchant,location,time = line.split(',')
        if user not in user8:
            user8.add(user)

with open('/home/wanghao/Document/tianchi/dataset/train9','rb') as f:
    for line in f :
        user,merchant,location,time = line.split(',')
        if user not in user9:
            user9.add(user)

with open('/home/wanghao/Document/tianchi/dataset/train10','rb') as f:
    for line in f :
        user,merchant,location,time = line.split(',')
        if user not in user10:
            user10.add(user)

with open('/home/wanghao/Document/tianchi/dataset/train11','rb') as f:
    for line in f :
        user,merchant,location,time = line.split(',')
        if (user,location) not in user11:
            user11.add((user,location))

user12 = set()
with open('/home/wanghao/Document/tianchi/dataset/trainfrom7to10','rb') as f:
    for line in f :
        line = line.strip('\r\n')
        user,merchant,location,time = line.split(',')
        if (user,location) not in user12:
            user12.add((user,location))

# print "7 & 12 " , len(user7 & user12)
# print "8 & 12 " , len(user8 & user12)
# print "9 & 12 " , len(user9 & user12)
# print "10 & 12 " , len(user10 & user12)
# print "11 & 12 " , len(user11 & user12)

print "11",len(user11)
print '7-10',len(user12)
print "jiaoji",len(user11&user12)
#
# a = 11
# if a > 10 :
#     print ">10"
# elif a == 0 :
#     print "== 0"
# else:
#     print "0<a<10"