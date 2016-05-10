import pickle

taobao_path = 'E:\IJCAI_competition\datasets\datasets\ijcai2016_taobao'

user_category ={}
user_time = {}
user_feature = {}
count = 1
with open(taobao_path) as f:
    for line in f:
        print "count:", count
        count += 1
        user,seller,item,category,action,time = line.split(',')
        if not user_feature.has_key(user):
            user_feature[user] = [0,0,0,0,0]
        if not user_category.has_key(user):
            user_category[user] = {}
        if not user_category[user].has_key(category):
            user_category[user][category] = [0,0]
        #print("action:",type(action),action)
        if action == '0':
            user_feature[user][0] += 1
            user_category[user][category][0] += 1
        else:
            user_feature[user][1] += 1
            user_category[user][category][1] += 1
        if not user_time.has_key(user):
            user_time[user] = []
        user_time[user].append(time)

#get {user:[#click,#buy,#num of different category with click action,#num of different category with buy action,#active days online]}
for user in user_feature:
    for category in user_category[user]:
        if user_category[user][category][0] > 1:
            user_feature[user][2] += 1
        if user_category[user][category][1] > 1:
            user_feature[user][3] += 1
    timelist = user_time[user]
    user_feature[user][4] = len(set(timelist))

outfile = 'E:\IJCAI_competition\datasets\datasets\user_feature_taobao.pkl'
output = open(outfile,'wb')
pickle.dump(user_feature,output)

