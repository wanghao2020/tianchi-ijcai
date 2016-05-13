import pickle
import datetime


class featureExtract():

    # month : [(uesr1, merchant1), (user1, merchant2)....]
    month_usermerchanttuple = {}
    user_feature = {}
    location_merchant_nums = {}
    def getMonthUserMerchantTuper(self, file, month):

        if not self.month_usermerchanttuple.has_key(month):
            self.month_usermerchanttuple[month] = []

        with open(file, 'rb') as f:
            count = 0
            for line in f :

                user, merchant, location, timstamp = line.split(',')
                tuple = (user, merchant)
                if tuple not in self.month_usermerchanttuple[month]:
                    self.month_usermerchanttuple[month].append(tuple)
                count += 1
                print count

        outfile = '/home/wanghao/Document/tianchi/dataset/userandmerchantTuple.pkl'
        with open(outfile, 'wb') as f :
            pickle.dump(self.month_usermerchanttuple, f)
            
    #get user_location {user:[loc1,loc2]}
    #get user_merchant_datetime {user:{merchant:[time1,time2...],..},...}
    def get_user_merchant_datetime(self,dataset):
        user_merchant_datetime = {}
        user_location = {}
        with open(dataset) as f:
            for line in f:
                line = line.strip('\r\n')
                user, merchant, location, time = line.split(',')
                if not user_merchant_datetime.has_key(user):
                    user_merchant_datetime[user] = {}
                if not user_merchant_datetime[user].has_key(merchant):
                    user_merchant_datetime[user][merchant] = []
                format_time = datetime.datetime.strptime(time,'%Y%m%d')
                user_merchant_datetime[user][merchant].append(format_time)
                if not user_location.has_key(user):
                    user_location[user] = []
                if location not in user_location[user]:
                    user_location[user].append(location)
        return user_merchant_datetime,user_location

    def get_location_merchant_nums(self,dataset):
        with open(dataset) as f:
            for line in f:
                line = line.strip('\r\n')
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

    def get_user_feature(self,dataset,startmonth,endmonth):
        user_merchant_datetime_all,user_location_all =  self.get_user_merchant_datetime(dataset)
        self.get_location_merchant_nums(dataset)
        print "get location_merchant_nums done!"
        user_merchant_datetime = {}
        user_location = {}
        i = 0
        for month in range(startmonth,endmonth+1):
            if endmonth-month+1 > 3:
                continue
            if month < 10:
                month = '0'+str(month)
            dataset_part = 'E:\IJCAI_competition\datasets\datasets\\trainfrom2015'+str(month)+'01to2015'+str(month)+'31'
            user_merchant_datetime[i] = {}
            user_location[i] ={}
            user_merchant_datetime[i],user_location[i] = self.get_user_merchant_datetime(dataset_part)
            i += 1
        count = 0
        for user in user_merchant_datetime_all:
            print "count:",count
            count += 1
            if not self.user_feature.has_key(user):
                self.user_feature[user] = [0] * 55 #?
            merchant_dict_all = user_merchant_datetime_all[user]
            active_days_all = []
            repeat_mer_nums_all = 0
            for mer in merchant_dict_all:
                # 0. the count of user visited all merchants
                self.user_feature[user][0] += len(merchant_dict_all[mer])
                active_days_all.extend(merchant_dict_all[mer])
                if len(merchant_dict_all[mer]) > 1:
                    repeat_mer_nums_all += 1
            # 8. num of all visited merchants
            self.user_feature[user][8] = len(merchant_dict_all)
            # 2. user active days offline
            self.user_feature[user][16] = len(set(active_days_all))
            active_days_all.sort()
            diff_days = []
            for i in range(len(active_days_all)-1):
                diff_days.append((active_days_all[i+1]-active_days_all[i]).days)
            if len(diff_days) >0:
                # 3. user max diff days offline
                self.user_feature[user][23] = max(diff_days)
                # 4. user min diff days offline
                self.user_feature[user][24] = min(diff_days)
                # 5. user avg diff days offline
                self.user_feature[user][25] = float(sum(diff_days))/len(diff_days)
            else:
                self.user_feature[user][23] = -1
                self.user_feature[user][24] = -1
                self.user_feature[user][25] = -1

            # 6. count of user visited location
            self.user_feature[user][26] = len(user_location_all[user])

            # 7. the count of user visited all merchants/user active days offline
            self.user_feature[user][33] = float(self.user_feature[user][0]) / self.user_feature[user][16]
            # num of merchants in loc where mer located
            mer_loc_nums_all = 0
            for loc in user_location_all[user]:
                mer_loc_nums_all += len(self.location_merchant_nums[loc])
            # 8. the number of user visited different merchants/count of all merchants local
            self.user_feature[user][40] = float(self.user_feature[user][8]) / mer_loc_nums_all

            # 9. num of repeat visited merchants / num of all visited merchants
            self.user_feature[user][48] = float(repeat_mer_nums_all) / self.user_feature[user][8]

            merchant_dict = {}
            active_days = []
            repeat_mer_nums = []
            visited_mer_count = []
            visited_mer_nums = []
            visited_loc_nums = []

            for i in range(len(user_merchant_datetime)):
                if user_merchant_datetime[i].has_key(user):
                    merchant_dict[i] = user_merchant_datetime[i][user]
                    active = []
                    visited_mer_count.append(0)
                    repeat_mer_nums.append(0)
                    for mer in merchant_dict[i]:
                        # 0. the count of user visited all merchants
                        visited_mer_count[i] += len(merchant_dict[i][mer])
                        active.extend(merchant_dict[i][mer])
                        if len(merchant_dict[i][mer]) > 1:
                            repeat_mer_nums[i] += 1

                    visited_mer_nums.append(len(merchant_dict[i]))
                    active_days.append(len(set(active)))
                    visited_loc_nums.append(len(user_location[i][user]))
                else:
                    visited_mer_count.append(0)
                    visited_mer_nums.append(0)
                    active_days.append(0)
                    visited_loc_nums.append(0)
                    repeat_mer_nums.append(0)

            self.user_feature[user][1] = visited_mer_count[0]
            self.user_feature[user][2] = visited_mer_count[1]
            self.user_feature[user][3] = visited_mer_count[2]
            self.user_feature[user][4] = float(self.user_feature[user][0])/(endmonth-startmonth+1)
            self.user_feature[user][5] = float(self.user_feature[user][0])/((endmonth-startmonth+1)*30)
            # increment num
            self.user_feature[user][6] = self.user_feature[user][2] - self.user_feature[user][1]
            self.user_feature[user][7] = self.user_feature[user][3] - self.user_feature[user][2]

            self.user_feature[user][9] = visited_mer_nums[0]
            self.user_feature[user][10] = visited_mer_nums[1]
            self.user_feature[user][11] = visited_mer_nums[2]
            self.user_feature[user][12] = float(self.user_feature[user][8])/(endmonth-startmonth+1)
            self.user_feature[user][13] = float(self.user_feature[user][8])/((endmonth-startmonth+1)*30)
            # increment num
            self.user_feature[user][14] = self.user_feature[user][10] - self.user_feature[user][9]
            self.user_feature[user][15] = self.user_feature[user][11] - self.user_feature[user][10]

            self.user_feature[user][17] = active_days[0]
            self.user_feature[user][18] = active_days[1]
            self.user_feature[user][19] = active_days[2]
            self.user_feature[user][20] = float(self.user_feature[user][16])/(endmonth-startmonth+1)
            # increment num
            self.user_feature[user][21] = self.user_feature[user][18] - self.user_feature[user][17]
            self.user_feature[user][22] = self.user_feature[user][19] - self.user_feature[user][18]

            self.user_feature[user][27] = visited_loc_nums[0]
            self.user_feature[user][28] = visited_loc_nums[1]
            self.user_feature[user][29] = visited_loc_nums[2]
            self.user_feature[user][30] = float(self.user_feature[user][26])/(endmonth-startmonth+1)
            # increment num
            self.user_feature[user][31] = self.user_feature[user][28] - self.user_feature[user][27]
            self.user_feature[user][32] = self.user_feature[user][29] - self.user_feature[user][28]
            if self.user_feature[user][17]:
                self.user_feature[user][34] = float(self.user_feature[user][1])/self.user_feature[user][17]
            else:
                self.user_feature[user][34] = -1
            if self.user_feature[user][18]:
                self.user_feature[user][35] = float(self.user_feature[user][2])/self.user_feature[user][18]
            else:
                self.user_feature[user][35] = -1
            if self.user_feature[user][19]:
                self.user_feature[user][36] = float(self.user_feature[user][3])/self.user_feature[user][19]
            else:
                self.user_feature[user][36] = -1
            if self.user_feature[user][20]:
                self.user_feature[user][37] = float(self.user_feature[user][4])/self.user_feature[user][20]
            else:
                self.user_feature[user][37] = -1
            if self.user_feature[user][21]:
                self.user_feature[user][38] = float(self.user_feature[user][6])/self.user_feature[user][21]
            else:
                self.user_feature[user][38] = -1
            if self.user_feature[user][22]:
                self.user_feature[user][39] = float(self.user_feature[user][7])/self.user_feature[user][22]
            else:
                self.user_feature[user][39] = -1

            self.user_feature[user][41] = float(self.user_feature[user][9]) / mer_loc_nums_all
            self.user_feature[user][42] = float(self.user_feature[user][10]) / mer_loc_nums_all
            self.user_feature[user][43] = float(self.user_feature[user][11]) / mer_loc_nums_all
            self.user_feature[user][44] = float(self.user_feature[user][12]) / mer_loc_nums_all
            self.user_feature[user][45] = float(self.user_feature[user][13]) / mer_loc_nums_all
            self.user_feature[user][46] = float(self.user_feature[user][14]) / mer_loc_nums_all
            self.user_feature[user][47] = float(self.user_feature[user][15]) / mer_loc_nums_all

            if self.user_feature[user][9]:
                self.user_feature[user][49] = float(repeat_mer_nums[0]) / self.user_feature[user][9]
            else:
                self.user_feature[user][49] = -1
            if self.user_feature[user][10]:
                self.user_feature[user][50] = float(repeat_mer_nums[1]) / self.user_feature[user][10]
            else:
                self.user_feature[user][50] = -1
            if self.user_feature[user][11]:
                self.user_feature[user][51] = float(repeat_mer_nums[2]) / self.user_feature[user][11]
            else:
                self.user_feature[user][51] = -1
            if self.user_feature[user][12]:
                self.user_feature[user][52] = float(repeat_mer_nums[0]+repeat_mer_nums[1]+repeat_mer_nums[2])/ 3 / self.user_feature[user][12]
            else:
                self.user_feature[user][52] = -1
            if self.user_feature[user][14]:
                self.user_feature[user][53] = float(repeat_mer_nums[1] - repeat_mer_nums[0]) / self.user_feature[user][14]
            else:
                self.user_feature[user][53] = -1
            if self.user_feature[user][15]:
                self.user_feature[user][54] = float(repeat_mer_nums[2] - repeat_mer_nums[1]) / self.user_feature[user][15]
            else:
                self.user_feature[user][54] = -1



if __name__ == '__main__':
    ft = featureExtract()
    file = 'E:\IJCAI_competition\datasets\datasets\ijcai2016_koubei_train'
    ft.get_user_feature(file,7,11)
    outfile = 'E:\IJCAI_competition\datasets\datasets\user_feature_from7to11.pkl'
    f = open(outfile,'wb')
    pickle.dump(ft.user_feature,f)
    key = ft.user_feature.keys()
    print ft.user_feature[key[0]]
    #pass