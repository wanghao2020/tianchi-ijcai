import pickle
import datetime
import time
from itertools import islice
taobao_path = '/home/wanghao/Document/tianchi/dataset/taobaofrom20150701to20150930'

user_item = {}
user_category ={}
user_seller = {}
user_action_nums = {}
user_time = {}
user_diff_time = {}
user_feature = {}
count = 1
with open(taobao_path) as f:
    for line in islice(f,1,None):
        print "count:", count
        count += 1
        line = line.strip('\r\n')
        user,seller,item,category,action,time = line.split(',')
        # print type(time)
        # print "time:" , time
        if not user_feature.has_key(user):
            user_feature[user] = [0] * 18
        if not user_item.has_key(user):
            user_item[user] = {}
        if not user_item[user].has_key(item):
            user_item[user][item] = [0,0]
        if not user_category.has_key(user):
            user_category[user] = {}
        if not user_category[user].has_key(category):
            user_category[user][category] = [0,0]
        if not user_seller.has_key(user):
            user_seller[user] = {}
        if not user_seller[user].has_key(seller):
            user_seller[user][seller] = [0,0]
        if not user_action_nums.has_key(user):
            user_action_nums[user] = [0,0]
        #print("action:",type(action),action)
        if action == '0':
            user_item[user][item][0] += 1
            user_category[user][category][0] += 1
            user_seller[user][seller][0] += 1
            user_action_nums[user][0] += 1
        else:
            user_item[user][item][1] += 1
            user_category[user][category][1] += 1
            user_seller[user][seller][1] += 1
            user_action_nums[user][1] += 1
        if not user_time.has_key(user):
            user_time[user] = []
        format_time = datetime.datetime.strptime(time,'%Y%m%d')
        user_time[user].append(format_time)
        user_time[user].sort()

#get {user:[,,,,]}
for user in user_feature:

    ## get user_item feature
    for item in user_item[user]:
        if user_item[user][item][0] > 0:
            # 0. num of different item with click action
            user_feature[user][0] += 1
            if user_item[user][item][0] > 1:
                # 10. num of repeat click different item
                user_feature[user][10] += 1
        if user_item[user][item][1] > 0:
            # 1. num of different item with buy action
            user_feature[user][1] += 1
            if user_item[user][item][1] > 1:
                # 11. num of repeat buy different item
                user_feature[user][11] += 1

    ## get user_category feature
    for category in user_category[user]:
        if user_category[user][category][0] > 0:
            # 2. num of different category with click action
            user_feature[user][2] += 1
            if user_category[user][category][0] > 1:
                # 12. num of repeat click different category
                user_feature[user][12] += 1
        if user_category[user][category][1] > 0:
            # 3. num of different category with buy action
            user_feature[user][3] += 1
            if user_category[user][category][1] > 1:
                # 13. num of repeat buy different category
                user_feature[user][13] += 1

    ## get user_seller feature
    for seller in user_seller[user]:
        if user_seller[user][seller][0] > 0:
            # 4. num of different seller with click action
            user_feature[user][4] += 1
            if user_seller[user][seller][0] > 1:
                # 14. num of repeat click different seller
                user_feature[user][14] += 1
        if user_seller[user][seller][1] > 0:
            # 5. num of different seller with buy action
            user_feature[user][5] += 1
            if user_seller[user][seller][1] > 1:
                # 15. num of repeat buy different seller
                user_feature[user][15] += 1

    ## get the user_time feature
    timelist = user_time[user]
    # 6. active days online
    user_feature[user][6] = len(set(timelist))
    if not user_diff_time.has_key(user):
        user_diff_time[user] = []
    for i in range(len(user_time[user])-1):
        user_diff_time[user].append((user_time[user][i+1] - user_time[user][i]).days)
    if len(user_diff_time[user]) > 0:
        # 7. max diff days
        user_feature[user][7] = max(user_diff_time[user])
        # 8. min diff days
        user_feature[user][8] = min(user_diff_time[user])
        # 9. avg diff days
        user_feature[user][9] = float(sum(user_diff_time[user])) / len(user_diff_time[user])
    else:
        user_feature[user][7] = -1
        user_feature[user][8] = -1
        user_feature[user][9] = -1

    # 16. total click nums
    user_feature[user][16] = user_action_nums[user][0]

    # 17. total buy nums
    user_feature[user][17] = user_action_nums[user][1]

outfile = '/home/wanghao/Document/tianchi/feature/user_feature_taobao_test.pkl'
output = open(outfile,'wb')
pickle.dump(user_feature,output)

