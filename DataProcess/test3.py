import pickle
import datetime
import csv


file = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_koubei_train'
wfile = open('/home/wanghao/user_merchants', 'wb')
writer = csv.writer(wfile)
user_merchants = {}
with open(file, 'rb') as f :
    for line in f :
        line = line.strip('\r\n')
        user,merchant,location,time = line.split(',')
        if not user_merchants.has_key(user):
            user_merchants[user] = {}
        if not user_merchants[user].has_key(location):
            user_merchants[user][location] = []
        if merchant not in user_merchants[user][location]:
            user_merchants[user][location].append(merchant)

user_count = 0
location_count = 0
merchant_count = 0

location1_count = 0
location2_count = 0
location3_count = 0
location4_count = 0


merchant1_count = 0
merchant2_count = 0
merchant3_count = 0
merchant4_count = 0
merchant5_count = 0


for user in user_merchants:
    user_count += 1
    result = []
    result.append(user)
    locationlist = []

    tmp1 = 0
    tmp2 = 0
    for loc in user_merchants[user]:

        merchants = user_merchants[user][loc]

        location_count += 1
        merchant_count += len(merchants)

        tmp1 += 1
        tmp2 += len(merchants)

        locationlist.append(loc)
        locationlist.append(merchants)

    result.append(locationlist)

    if tmp1 == 1:
        location1_count += 1

    if tmp1 == 2:
        location2_count += 1
        writer.writerow(result)

    if tmp1 == 3:
        location3_count += 1
        writer.writerow(result)

    if tmp1 == 4:
        location4_count += 1
        writer.writerow(result)

    if tmp2 == 1 :
        merchant1_count += 1

    if tmp2 == 2:
        merchant2_count += 1

    if tmp2 == 3:
        merchant3_count += 1

    if tmp2 == 4:
        merchant4_count += 1

    if tmp2 == 5:
        merchant5_count += 1


    # writer.writerow(result)

print 'avg location', location_count/float(user_count)
print 'avg merchant', merchant_count/float(user_count)
print 'usercount', user_count
print 'only one location user', location1_count,' percentage:' , location1_count / float(user_count)
print 'only two location user', location2_count,' percentage:' , location2_count / float(user_count)
print 'only three location user', location3_count,' percentage:' , location3_count / float(user_count)
print 'only four location user', location4_count,' percentage:' , location4_count / float(user_count)

print 'only one merchant user:',merchant1_count,' percentage:', merchant1_count / float(user_count)
print 'only two merchant user:',merchant2_count,' percentage:', merchant2_count / float(user_count)
print 'only three merchant user:',merchant3_count,' percentage:', merchant3_count / float(user_count)
print 'only four merchant user:',merchant4_count,' percentage:', merchant4_count / float(user_count)
print 'only five merchant user:',merchant5_count,' percentage:', merchant5_count / float(user_count)
# writer.writerows(user_merchants)
wfile.close()