from GetFeature import feature
import pickle
import csv
#
# file = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_koubei_train'
# wfile = open('/home/wanghao/location_merchant_precentage', 'wb')
# writer = csv.writer(wfile)
#
# location_merchant_people = {}
# with open(file, 'rb') as f :
#     for line in f:
#         line = line.strip('\r\n')
#         user,merchant,location,time = line.split(',')
#         if not location_merchant_people.has_key(location):
#             location_merchant_people[location] = {}
#         if not location_merchant_people[location].has_key(merchant):
#             location_merchant_people[location][merchant] = []
#         if user not in location_merchant_people[location][merchant]:
#             location_merchant_people[location][merchant].append(user)
#
# location_merchant_percentage = {}
# for loc in location_merchant_people:
#     location_merchant_percentage[loc] = {}
#     locationpeople = set()
#     for mer in location_merchant_people[loc]:
#         for user in location_merchant_people[loc][mer]:
#             locationpeople.add(user)
#
#     for mer in location_merchant_people[loc]:
#         location_merchant_percentage[loc][mer] = len(location_merchant_people[loc][mer]) / float(len(locationpeople))
#
# for loc in location_merchant_percentage:
#     result = []
#     result.append(loc)
#
#     for mer in location_merchant_percentage[loc]:
#         result.append((mer,location_merchant_percentage[loc][mer]))
#     writer.writerow(result)
#
#
#
# wfile.close()
#-------------
# taobaofile = '/home/wanghao/Document/tianchi/dataset/TaoBaoClean'
# merchantfile = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_koubei_train'
# userset = set()
# with open(file,'rb') as f :
#     for line in f :
#         user = line.strip('\r\n').split(',')[0]
#         userset.add(user)
#
# print 'length',len(userset)
#--------------
taobaofile = '/home/wanghao/Document/tianchi/dataset/TaoBaoClean'
merchantfile = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_koubei_train'
wfile = open('/home/wanghao/merchant_user','wb')
merchant_users = {}
with open(merchantfile, 'rb') as f :
    for line in f :
        line = line.strip('\r\n')
        user,merchant,location,time = line.split(',')
        if not merchant_users.has_key(merchant):
            merchant_users[merchant] = []
        if user not in merchant_users[merchant]:
            merchant_users[merchant].append(user)
writer = csv.writer(wfile)
for mer in merchant_users:
    result = []
    result.append(mer)
    result.append(':')
    for user in merchant_users[mer]:
        result.append(user)
    writer.writerow(result)

wfile.close()
merchantusers  = merchant_users['275']
user_item = {}
user_seller = {}
user_category = {}
with open(taobaofile, 'rb') as f :
    for line in f :
        line = line.strip('\r\n')
        user,seller,item,category,onaction,time = line.split(',')
        if int(onaction) == 1:

            if not user_category.has_key(user):
                user_category[user]= []
            if not user_item.has_key(user):
                user_item[user] = []
            if not user_seller.has_key(user):
                user_seller[user] = []
            if category not in user_category[user]:
                user_category[user].append(category)
            if item not in user_item[user]:
                user_item[user].append(item)
            if seller not in user_seller[user]:
                user_seller[user].append(seller)

print '*'*50
print 'item similarity'
for user in merchantusers:
    if not user_item.has_key(user):
        print user, '      '
    else:
        print user, '  ', user_item[user]

print '*'*50
print 'category similarity'
for user in merchantusers:
    if not user_category.has_key(user):
        print user, '      '
    else:
        print user,'  ' ,user_category[user]

print '*' * 50
print 'seller similarity'
for user in merchantusers:
    if not user_seller.has_key(user):
        print user, '    '
    else:
        print user, '  ',user_seller[user]
