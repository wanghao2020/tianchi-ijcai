import pickle
import numpy as np
import datetime
import time
from itertools import islice
train_path = 'E:\IJCAI_competition\datasets\datasets\model_train.csv'
label_path = 'E:\IJCAI_competition\datasets\datasets\model_label.csv'
test_path = 'E:\IJCAI_competition\datasets\datasets\model_test.csv'

#train_path = '/home/wanghao/Document/tianchi/datasets/model_train.csv'
#label_path = '/home/wanghao/Document/tianchi/datasets/model_label.csv'
#test_path = '/home/wanghao/Document/tianchi/datasets/model_test.csv'

class feature:
    location_merchant_nums = {}
    location_passenger_flow = {}
    location_merchant_regular_customer_nums = {}
    user_merchant_datetime = {}
    user_location = {}
    merchant_feature = {}
    user_feature = {}
    UM_feature = {}
    label_list = []


    def get_location_merchant_nums(self,dataset):
        location_merchant_users ={}
        with open(dataset) as f:
            for line in islice(f,1,None):
                line = line.strip('\n')
                user,merchant,location,time = line.split(',')
                #  get the {location : { merchant : visted nums }}
                if self.location_merchant_nums.has_key(location):
                    merchant_nums = self.location_merchant_nums[location]
                    if merchant_nums.has_key(merchant):
                        merchant_nums[merchant] = merchant_nums[merchant] + 1
                    else:
                        merchant_nums[merchant] = 1
                else:
                    merchant_nums = {}
                    merchant_nums[merchant] = 1
                    self.location_merchant_nums[location] = merchant_nums

                if not location_merchant_users.has_key(location):
                    location_merchant_users[location] = {}
                if not location_merchant_users[location].has_key(merchant):
                    location_merchant_users[location][merchant] = []
                location_merchant_users[location][merchant].append(user)

                #get user_location {user:[loc1,loc2]}
                #get user_merchant_datetime {user:{merchant:[time1,time2...],..},...}
                if not self.user_merchant_datetime.has_key(user):
                    self.user_merchant_datetime[user] = {}
                if not self.user_merchant_datetime[user].has_key(merchant):
                    self.user_merchant_datetime[user][merchant] = []
                format_time = datetime.datetime.strptime(time,'%Y-%m-%d')
                self.user_merchant_datetime[user][merchant].append(format_time)
                if not self.user_location.has_key(user):
                    self.user_location[user] = []
                if location not in self.user_location[user]:
                    self.user_location[user].append(location)

        # get the {location:{merchant:[ frequent_customer_num, all_customer_num ]}}
        for loc in location_merchant_users:
            self.location_merchant_regular_customer_nums[loc] = {}
            for mer in location_merchant_users[loc]:
                self.location_merchant_regular_customer_nums[loc][mer] = [0, 0]
                user_list = location_merchant_users[loc][mer]
                for usr in user_list:
                    if user_list.count(usr) > 1:
                        self.location_merchant_regular_customer_nums[loc][mer][0] += 1
                self.location_merchant_regular_customer_nums[loc][mer][1] = len(set(user_list))


    # get the { location : passengerflow} from trainfile
    def get_location_passenger_flow(self,dataset):
        self.get_location_merchant_nums(dataset)
        for loc in self.location_merchant_nums:
            self.location_passenger_flow[loc] = 0
            for mer in self.location_merchant_nums[loc]:
                self.location_passenger_flow[loc] = self.location_passenger_flow[loc] + self.location_merchant_nums[loc][mer]
    
    #
    def get_location_merchant_users(self,dataset):

        location_merchant_users ={}

        # get the {  location: {merchant ; [user1, user2,...userN]} }
        with open(dataset) as f:
            for line in islice(f,1,None):
                user, merchant, location, time = line.split(',')
                if not location_merchant_users.has_key(location):
                    location_merchant_users[location] = {}
                if not location_merchant_users[location].has_key(merchant):
                    location_merchant_users[location][merchant] = []
                location_merchant_users[location][merchant].append(user)

        # get the {location:{merchant:[ frequent_customer_num, all_customer_num ]}}
        for loc in location_merchant_users:
            self.location_merchant_regular_customer_nums[loc] = {}
            for mer in location_merchant_users[loc]:
                self.location_merchant_regular_customer_nums[loc][mer] = [0, 0]
                user_list = location_merchant_users[loc][mer]
                for usr in user_list:
                    if user_list.count(usr) > 1:
                        self.location_merchant_regular_customer_nums[loc][mer][0] += 1
                self.location_merchant_regular_customer_nums[loc][mer][1] = len(set(user_list))

    #get merchant_feature {merchant:[x0,..,x5],...}
    def get_location_merchant_feature(self,dataset):
        print "get location_merchant feature..."
        self.get_location_passenger_flow(dataset)
        #self.get_location_merchant_nums(dataset)
        with open(dataset) as f:
            for line in islice(f,1,None):
                user,mer,loc,time = line.split(',')
                if not self.merchant_feature.has_key((loc,mer)):

                    self.merchant_feature[(loc,mer)] = [0] * 7

                # 0. merchant all mer's passenger flow
                self.merchant_feature[(loc,mer)][0] = self.merchant_feature[(loc,mer)][0] + 1

                # 1. merchant location passenger flow
                self.merchant_feature[(loc,mer)][1] = self.location_merchant_nums[loc][mer]

                # 2. the sum of passenger flow of all merchants in loc which merchant mer located
                self.merchant_feature[(loc,mer)][2] = self.location_passenger_flow[loc]

                if self.location_merchant_nums.has_key(loc):
                    # 3. count of merchants in which mer located
                    self.merchant_feature[(loc,mer)][3] = len(self.location_merchant_nums[loc])
                    # 6. the rate of regular customer
                    self.merchant_feature[(loc,mer)][6] = float(self.location_merchant_regular_customer_nums[loc][mer][0]) / self.location_merchant_regular_customer_nums[loc][mer][1]

                # 4. passenger flow of mer / the sum of passenger flow local
                self.merchant_feature[(loc,mer)][4] = float(self.merchant_feature[(loc,mer)][1]) / self.merchant_feature[(loc,mer)][2]
                # 5. average passenger flow local
                self.merchant_feature[(loc,mer)][5] = float(self.merchant_feature[(loc,mer)][2]) / self.merchant_feature[(loc,mer)][3]

    #get user_location {user:[loc1,loc2]}
    #get user_merchant_datetime {user:{merchant:[time1,time2...],..},...}
    def get_user_merchant_datetime(self,dataset):
        with open(dataset) as f:
            for line in islice(f,1,None):
                line = line.strip('\n')
                user, merchant, location, time = line.split(',')
                if not self.user_merchant_datetime.has_key(user):
                    self.user_merchant_datetime[user] = {}
                if not self.user_merchant_datetime[user].has_key(merchant):
                    self.user_merchant_datetime[user][merchant] = []
                format_time = datetime.datetime.strptime(time,'%Y-%m-%d')
                self.user_merchant_datetime[user][merchant].append(format_time)
                if not self.user_location.has_key(user):
                    self.user_location[user] = []
                if location not in self.user_location[user]:
                    self.user_location[user].append(location)

    #get user_feature {user:[x0,...,x43],...}
    def get_user_feature(self,dataset):
        print "get user feature..."
        plk_file = open('E:\IJCAI_competition\datasets\datasets\user_feature_taobao_test.pkl','rb')
        user_feature_taobao = pickle.load(plk_file)
        self.get_user_merchant_datetime(dataset)
        for user in self.user_merchant_datetime:
            if not self.user_feature.has_key(user):
                self.user_feature[user] = [0 for i in range(43)]
            merchant_dict = self.user_merchant_datetime[user]
            active_days = []
            repeat_mer_nums = 0
            for mer in merchant_dict:
                # 0. the count of user visited all merchants
                self.user_feature[user][0] += len(merchant_dict[mer])
                active_days.extend(merchant_dict[mer])
                if len(merchant_dict[mer]) > 1:
                    repeat_mer_nums += 1
            # 1. num of all visited merchants
            self.user_feature[user][1] = len(merchant_dict)
            # 9. user active days offline
            self.user_feature[user][9] = len(set(active_days))
            active_days.sort()
            diff_days = []
            for i in range(len(active_days)-1):
                diff_days.append((active_days[i+1]-active_days[i]).days)
            if len(diff_days) >0:
                # 13. user max diff days offline
                self.user_feature[user][13] = max(diff_days)
                # 14. user min diff days offline
                self.user_feature[user][14] = min(diff_days)
                # 15. user avg diff days offline
                self.user_feature[user][15] = float(sum(diff_days))/len(diff_days)
            else:
                self.user_feature[user][13] = -1
                self.user_feature[user][14] = -1
                self.user_feature[user][15] = -1

            # 16. count of user visited location
            self.user_feature[user][16] = len(self.user_location[user])

            # 22. the count of user visited all merchants/user active days offline
            self.user_feature[user][22] = float(self.user_feature[user][0]) / self.user_feature[user][9]
            # num of merchants in loc where mer located
            mer_loc_nums = 0
            for loc in self.user_location[user]:
                mer_loc_nums += len(self.location_merchant_nums[loc])
            # 23. the number of user visited different merchants/count of all merchants local
            self.user_feature[user][23] = float(self.user_feature[user][1]) / mer_loc_nums

            # 36. num of repeat visited merchants / num of all visited merchants
            self.user_feature[user][36] = float(repeat_mer_nums) / self.user_feature[user][1]

            if user_feature_taobao.has_key(user):
                # 2. user click number
                self.user_feature[user][2] = user_feature_taobao[user][0]
                # 3. user buy number
                self.user_feature[user][3] = user_feature_taobao[user][1]
                # 4. number of user click different category
                self.user_feature[user][4] = user_feature_taobao[user][2]
                # 5. number of user buy different category
                self.user_feature[user][5] = user_feature_taobao[user][3]
                # 6. number of user click different seller
                self.user_feature[user][6] = user_feature_taobao[user][4]
                # 7. number of user buy different seller
                self.user_feature[user][7] = user_feature_taobao[user][5]
                # 8 .user active days online
                self.user_feature[user][8] = user_feature_taobao[user][6]
                # 10. user max diff days online
                self.user_feature[user][10] = user_feature_taobao[user][7]
                # 11. user min diff days online
                self.user_feature[user][11] = user_feature_taobao[user][8]
                # 12. user avg diff days online
                self.user_feature[user][12] = user_feature_taobao[user][9]

                # 17. total click num
                self.user_feature[user][17] = user_feature_taobao[user][16]
                # 18. total buy num
                self.user_feature[user][18] = user_feature_taobao[user][17]

                # 19. buy num / click num (different item)
                self.user_feature[user][19] = float(self.user_feature[user][3] + 1) / (self.user_feature[user][2] + 1)
                # 20. buy num / click num (different category)
                self.user_feature[user][20] = float(self.user_feature[user][5] + 1) / (self.user_feature[user][4] + 1)
                # 21.buy num / click num (different seller)
                self.user_feature[user][21] = float(self.user_feature[user][7] + 1) / (self.user_feature[user][6] + 1)

                # 24. number of user click different category /active days online
                self.user_feature[user][24] = float(self.user_feature[user][4]) / self.user_feature[user][8]
                # 25. number of user buy different category / active days online
                self.user_feature[user][25] = float(self.user_feature[user][5]) / self.user_feature[user][8]
                # 26. number of user click different item / active days online
                self.user_feature[user][26] = float(self.user_feature[user][2]) / self.user_feature[user][8]
                # 27. number of user buy different item / active days online
                self.user_feature[user][27] = float(self.user_feature[user][3]) / self.user_feature[user][8]
                # 28. number of user click different seller / active days online
                self.user_feature[user][28] = float(self.user_feature[user][6]) / self.user_feature[user][8]
                # 29. number of user buy different seller / active days online
                self.user_feature[user][29] = float(self.user_feature[user][7]) / self.user_feature[user][8]


                # 30. num of repeat click item / all num of click item
                self.user_feature[user][30] = float(user_feature_taobao[user][10] + 1) / (user_feature_taobao[user][0] + 1)
                # 31. num of repeat buy item / all num of buy item
                self.user_feature[user][31] = float(user_feature_taobao[user][11] + 1) / (user_feature_taobao[user][1] + 1)
                # 32. num of repeat click category / all num of click category
                self.user_feature[user][32] = float(user_feature_taobao[user][12] + 1) / (user_feature_taobao[user][2] + 1)
                # 33. num of repeat buy category / all num of buy category
                self.user_feature[user][33] = float(user_feature_taobao[user][13] + 1) / (user_feature_taobao[user][3] + 1)
                # 34. num of repeat click seller / all num of click seller
                self.user_feature[user][34] = float(user_feature_taobao[user][14] + 1) / (user_feature_taobao[user][4] + 1)
                # 35. num of repeat buy seller / all num of buy seller
                self.user_feature[user][35] = float(user_feature_taobao[user][15] + 1) / (user_feature_taobao[user][5] + 1)


                # 37. number of user click different category / total click num
                self.user_feature[user][37] = float(self.user_feature[user][4] + 1) / (user_feature_taobao[user][16] + 1)
                # 38. number of user buy different category / total buy num
                self.user_feature[user][38] = float(self.user_feature[user][5] + 1) / (user_feature_taobao[user][17] + 1)
                # 39. number of user click different item / total click num
                self.user_feature[user][39] = float(self.user_feature[user][2] + 1) / (user_feature_taobao[user][16] + 1)
                # 40. number of user buy different item / total buy num
                self.user_feature[user][40] = float(self.user_feature[user][3] + 1) / (user_feature_taobao[user][17] + 1)
                # 41. number of user click different seller / total click num
                self.user_feature[user][41] = float(self.user_feature[user][6] + 1) / (user_feature_taobao[user][16] + 1)
                # 42. number of user buy different seller / total buy num
                self.user_feature[user][42] = float(self.user_feature[user][7] + 1) / (user_feature_taobao[user][17] + 1)

    #get UM_feature {[user,merchant]:[x0,...,x9],...}
    def get_user_merchant_feature(self,dataset):
        print "get user_merchant feature..."
        UM_time = {}
        with open(dataset) as f:
            for line in islice(f,1,None):
                line = line.strip('\n')
                user, merchant, location, time = line.split(',')
                UM_pair = (user,merchant)
                if not self.UM_feature.has_key(UM_pair):
                    self.UM_feature[UM_pair] = [0] * 9
                # 0. count of user visited merchant A
                self.UM_feature[UM_pair][0] += 1
                if not UM_time.has_key(UM_pair):
                    UM_time[UM_pair] = []
                format_time = datetime.datetime.strptime(time,'%Y-%m-%d')
                UM_time[UM_pair].append(format_time)
        for key in self.UM_feature:
            # 1. days of user visited merchant A
            self.UM_feature[key][1] = len(set(UM_time[key]))
            diff_days = []
            for i in range(len(UM_time[key])-1):
                diff_days.append((UM_time[key][i+1]-UM_time[key][i]).days)
            if len(diff_days) > 0:
                # 2. max diff days
                self.UM_feature[key][2] = max(diff_days)
                # 3. min diff days
                self.UM_feature[key][3] = min(diff_days)
                # 4. avg diff days
                self.UM_feature[key][4] = float(sum(diff_days))/len(diff_days)
            else:
                self.UM_feature[key][2] = -1
                self.UM_feature[key][3] = -1
                self.UM_feature[key][4] = -1

            # 5. count of user visited merchant A / count of user visited all merchants
            self.UM_feature[key][5] = float(self.UM_feature[key][0])/self.user_feature[key[0]][0]
            mer_passenger_flow = 0
            for loc in self.location_merchant_nums:
                if key[1] in self.location_merchant_nums[loc]:
                    mer_passenger_flow += self.location_merchant_nums[loc][key[1]]
            # 6. count of user visited merchant A / passenger flow of merchant A
            self.UM_feature[key][6] = float(self.UM_feature[key][0]) / mer_passenger_flow

            # 7. days of user visited merchant A / user active days offline
            self.UM_feature[key][7] = float(self.UM_feature[key][1]) / self.user_feature[key[0]][9]
            # 8. count of user visited merchant A / user active days offline
            self.UM_feature[key][8] = float(self.UM_feature[key][0]) / self.user_feature[key[0]][9]


    #get label_list [user,merchant]
    def get_label_list(self,dataset):
        print "get_label_list..."
        with open(dataset) as f:
            for line in islice(f,1,None):
                user,merchant,location,time = line.split(',')
                if (user,merchant) not in self.label_list:
                    self.label_list.append((user,merchant))

if __name__ == '__main__':

    f = feature()
    f.get_location_merchant_feature(train_path)
    f.get_user_feature(train_path)
    f.get_user_merchant_feature(train_path)
    f.get_label_list(label_path)
    sample = []
    label = []
    UML_pair = []
    with open(train_path) as f:
        for line in f:
            user,merchant,loction,time = line.split(',')
            if (user,merchant,loction) not in UML_pair:
                UML_pair.append((user,merchant,location))
                sam = []
                sam.extend(f.merchant_feature[(loction,merchant)])
                sam.extend(f.user_feature[user])
                sam.extend(f.UM_feature[(user,merchant)])
            UML_pair.append(sam)
            if (user,merchant) in f.label_list:
                label.append(1)
            else:
                label.append(0)
    print "get feature done!"
    outfile = open('E:\IJCAI_competition\datasets\datasets\sample.pkl','wb')
    pickle.dump(sample,outfile)
    outfile2 = open('E:\IJCAI_competition\datasets\datasets\label.pkl','wb')
    pickle.dump(label,outfile2)
