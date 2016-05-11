import pickle
import numpy as np

#sample_path = 'E:\IJCAI_competition\datasets\datasets\model_train.csv'
#label_path = 'E:\IJCAI_competition\datasets\datasets\model_label.csv'
#test_path = 'E:\IJCAI_competition\datasets\datasets\model_test.csv'

train_path = '/home/wanghao/Document/tianchi/datasets/model_train.csv'
label_path = '/home/wanghao/Document/tianchi/datasets/model_label.csv'
test_path = '/home/wanghao/Document/tianchi/datasets/model_test.csv'

class feature:
    location_merchant_nums = {}
    location_passenger_flow = {}
    location_merchant_regular_customer_nums = {}
    merchant_feature = {}
    user_feature = {}
    UM_feature = {}
    label = []

    #  get the {location : { merchant : visted nums }} from trainfile
    def get_location_merchant_nums(self,dataset):
        with open(dataset) as f:
            for line in f:
                linelist = line.split(',')
                location = linelist[2]
                merchant = linelist[1]
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
    
    # get the { location : passengerflow} from trainfile
    def get_location_passenger_flow(self,dataset):
        self.get_location_merchant_nums(dataset)
        for loc in self.location_merchant_nums:
            self.location_passenger_flow[loc] = 0
            for mer in self.location_merchant_nums[loc]:
                self.location_passenger_flow[loc] = self.location_passenger_flow[loc] + self.location_merchant_nums[loc][mer]
    
    #
    def get_location_merchant_user_nums(self,dataset):

        location_merchant_users ={}

        # get the {  location: {merchant ; [user1, user2,...userN]} }
        with open(dataset) as f:
            for line in f:
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
        self.get_location_merchant_user_nums(dataset)
        with open(dataset) as f:
            for line in f:
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
                    self.merchant_feature[(loc,mer)][6] = self.location_merchant_regular_customer_nums[loc][mer][0] / self.location_merchant_regular_customer_nums[loc][mer][1]

                # 4. passenger flow of mer / the sum of passenger flow local
                self.merchant_feature[(loc,mer)][4] = self.merchant_feature[(loc,mer)][1]/self.merchant_feature[(loc,mer)][2]
                # 4. average passenger flow local
                self.merchant_feature[(loc,mer)][5] = self.merchant_feature[(loc,mer)][2]/self.merchant_feature[(loc,mer)][3]




    #get user_feature {user:[x0,...,x15],...}
    def get_user_feature(self,dataset):
        print "get user feature..."
        plk_file = open('/home/wanghao/Document/tianchi/datasets/user_feature_taobao.pkl','rb')
        user_feature_taobao = pickle.load(plk_file)
        user_merchant_datetime = {}
        with open(dataset) as f:
            for line in f:
                user, merchant, location, time = line.split(',')
                # user_merchant_datetime {user:{merchant:[time1,time2...],..},...}
                if not user_merchant_datetime.has_key(user):
                    user_merchant_datetime[user] = {}
                if not user_merchant_datetime[user].has_key(merchant):
                    user_merchant_datetime[user][merchant] = []
                user_merchant_datetime[user][merchant].append(time)
        for user in user_merchant_datetime:
            if not self.user_feature.has_key(user):
                self.user_feature[user] = [0 for i in range(16)]

            merchant_dict = user_merchant_datetime[user]
            active_days = []
            different_mer = 0
            for mer in merchant_dict:
                # the count of user visited all merchants
                self.user_feature[user][0] += len(merchant_dict[mer])
                active_days.extend(merchant_dict[mer])
                different_mer += self.merchant_feature[mer][0]
            # the count of user visited different merchants
            self.user_feature[user][1] = len(merchant_dict)
            # user active days offline
            self.user_feature[user][5] = len(set(active_days))
            # the count of user visited all merchants/user active days offline
            self.user_feature[user][10] = self.user_feature[user][0]/self.user_feature[user][5]
            # the count of user visited different merchants/count of all merchants local
            self.user_feature[user][11] = self.user_feature[user][1]/different_mer
            if user_feature_taobao.has_key(user):
                # user click number
                self.user_feature[user][2] = user_feature_taobao[user][0]
                # user buy number
                self.user_feature[user][3] = user_feature_taobao[user][1]
                # user active days online
                self.user_feature[user][4] = user_feature_taobao[user][4]
                # number of user click different category
                self.user_feature[user][6] = user_feature_taobao[user][2]
                # number of user buy different category
                self.user_feature[user][7] = user_feature_taobao[user][3]
                # user buy number / user click number
                if self.user_feature[user][2]:
                    self.user_feature[user][8] = self.user_feature[user][3]/self.user_feature[user][2]
                # buy num/click num (different category)
                if self.user_feature[user][6]:
                    self.user_feature[user][9] = self.user_feature[user][7]/self.user_feature[user][6]
                # number of user click different category/active days online
                self.user_feature[user][12] = self.user_feature[user][6]/self.user_feature[user][4]
                # number of user buy different category/ active days online
                self.user_feature[user][13] = self.user_feature[user][7]/self.user_feature[user][4]
                # user click num/active days online
                self.user_feature[user][14] = self.user_feature[user][2]/self.user_feature[user][4]
                # user buy num/active days online
                self.user_feature[user][15] = self.user_feature[user][3]/self.user_feature[user][4]



    #get UM_feature {[user,merchant]:[x0,...,x4],...}
    def get_user_merchant_feature(self,dataset):
        print "get user_merchant feature..."
        UM_time = {}
        with open(dataset) as f:
            for line in f:
                user, merchant, location, time = line.split(',')
                UM_pair = (user,merchant)
                if not self.UM_feature.has_key(UM_pair):
                    self.UM_feature[UM_pair] = [0,0,0,0]
                # count of user visited merchant A
                self.UM_feature[UM_pair][0] += 1
                if not UM_time.has_key(UM_pair):
                    UM_time[UM_pair] = []
                UM_time[UM_pair].append(time)
        for key in self.UM_feature:
            # count of user visited merchant A/count of user visited all merchants
            #print "user",key[0]
            #print "error:", self.user_feature[key[0]][0]
            self.UM_feature[key][1] = self.UM_feature[key][0]/self.user_feature[key[0]][0]
            # count of user visited merchant A/passenger flow of all merchants which merchant A located
            self.UM_feature[key][2] = self.UM_feature[key][0]/self.merchant_feature[key[1]][0]
            # days of user visited merchant A/active days offline
            self.UM_feature[key][3] = len(set(UM_time[key]))/self.user_feature[key[0]][5]

    #get label [user,merchant]
    def get_label(self,dataset):
        with open(dataset) as f:
            for line in f:
                user,merchant,location,time = line.split(',')
                if (user,merchant) not in self.label:
                    self.label.append((user,merchant))

if __name__ == '__main__':

    f = feature()
    f.get_merchant_feature(train_path)
    f.get_user_feature(train_path)
    f.get_user_merchant_feature(train_path)
    f.get_label(label_path)
    sample = np.zeros((len(f.UM_feature),26+1))

    i = 0
    for key in f.UM_feature:
        user = key[0]
        merchant = key[1]
        j = 0
        for k in range(6):
            sample[i][j] = f.merchant_feature[merchant][k]
            j += 1
            if key in f.label:
                sample[i][j] = 1
        for k in range(16):
            sample[i][j] = f.user_feature[user][k]
            j += 1
            if key in f.label:
                sample[i][j] = 1
        for k in range(4):
            sample[i][j] = f.UM_feature[key][k]
            j += 1

        # positive sample
        if key in f.label:
            sample[i][j] = 1
    outfile = open('/home/wanghao/Document/tianchi/datasets/sample.pkl','wb')

        #if key in f.label:
        #   sample[i][j] = 1

    #outfile = open('E:\IJCAI_competition\datasets\datasets\sample.pkl','wb')

    pickle.dump(sample,outfile)
