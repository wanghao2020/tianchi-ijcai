import pickle
import datetime
import time

class taobao_user_feature:

    user_item = {}
    user_category ={}
    user_seller = {}
    user_action_nums = {}
    user_time = {}
    user_diff_time = {}
    user_taobao_feature = {}

    def get_taobao_user_feature(self, taobao_path):

        with open(taobao_path) as f:
            for line in f:
                line = line.strip('\r\n')
                user,seller,item,category,action,time = line.split(',')

                if not self.user_taobao_feature.has_key(user):
                    self.user_taobao_feature[user] = [0] * 18

                if not self.user_item.has_key(user):
                    self.user_item[user] = {}
                if not self.user_item[user].has_key(item):
                    self.user_item[user][item] = [0,0]

                if not self.user_category.has_key(user):
                    self.user_category[user] = {}
                if not self.user_category[user].has_key(category):
                    self.user_category[user][category] = [0,0]

                if not self.user_seller.has_key(user):
                    self.user_seller[user] = {}
                if not self.user_seller[user].has_key(seller):
                    self.user_seller[user][seller] = [0,0]

                if not self.user_action_nums.has_key(user):
                    self.user_action_nums[user] = [0,0]

                #print("action:",type(action),action)
                if action == '0':
                    self.user_item[user][item][0] += 1
                    self.user_category[user][category][0] += 1
                    self.user_seller[user][seller][0] += 1
                    self.user_action_nums[user][0] += 1
                else:
                    self.user_item[user][item][1] += 1
                    self.user_category[user][category][1] += 1
                    self.user_seller[user][seller][1] += 1
                    self.user_action_nums[user][1] += 1

                if not self.user_time.has_key(user):
                    self.user_time[user] = []

                format_time = datetime.datetime.strptime(time,'%Y%m%d')
                self.user_time[user].append(format_time)
                self.user_time[user].sort()
        
        #get {user:[,,,,]}
        for user in self.user_taobao_feature:
        
            ## get self.user_item feature
            for item in self.user_item[user]:
                if self.user_item[user][item][0] > 0:
                    # 0. num of different item with click action
                    self.user_taobao_feature[user][0] += 1
                    if self.user_item[user][item][0] > 1:
                        # 10. num of repeat click different item
                        self.user_taobao_feature[user][10] += 1
                if self.user_item[user][item][1] > 0:
                    # 1. num of different item with buy action
                    self.user_taobao_feature[user][1] += 1
                    if self.user_item[user][item][1] > 1:
                        # 11. num of repeat buy different item
                        self.user_taobao_feature[user][11] += 1
        
            ## get self.user_category feature
            for category in self.user_category[user]:
                if self.user_category[user][category][0] > 0:
                    # 2. num of different category with click action
                    self.user_taobao_feature[user][2] += 1
                    if self.user_category[user][category][0] > 1:
                        # 12. num of repeat click different category
                        self.user_taobao_feature[user][12] += 1
                if self.user_category[user][category][1] > 0:
                    # 3. num of different category with buy action
                    self.user_taobao_feature[user][3] += 1
                    if self.user_category[user][category][1] > 1:
                        # 13. num of repeat buy different category
                        self.user_taobao_feature[user][13] += 1
        
            ## get self.user_seller feature
            for seller in self.user_seller[user]:
                if self.user_seller[user][seller][0] > 0:
                    # 4. num of different seller with click action
                    self.user_taobao_feature[user][4] += 1
                    if self.user_seller[user][seller][0] > 1:
                        # 14. num of repeat click different seller
                        self.user_taobao_feature[user][14] += 1
                if self.user_seller[user][seller][1] > 0:
                    # 5. num of different seller with buy action
                    self.user_taobao_feature[user][5] += 1
                    if self.user_seller[user][seller][1] > 1:
                        # 15. num of repeat buy different seller
                        self.user_taobao_feature[user][15] += 1
        
            ## get the self.user_time feature
            timelist = self.user_time[user]
            # 6. active days online
            self.user_taobao_feature[user][6] = len(set(timelist))
            if not self.user_diff_time.has_key(user):
                self.user_diff_time[user] = []
            for i in range(len(self.user_time[user])-1):
                self.user_diff_time[user].append((self.user_time[user][i+1] - self.user_time[user][i]).days)
            if len(self.user_diff_time[user]) > 0:
                # 7. max diff days
                self.user_taobao_feature[user][7] = max(self.user_diff_time[user])
                # 8. min diff days
                self.user_taobao_feature[user][8] = min(self.user_diff_time[user])
                # 9. avg diff days
                self.user_taobao_feature[user][9] = float(sum(self.user_diff_time[user])) / len(self.user_diff_time[user])
            else:
                self.user_taobao_feature[user][7] = -1
                self.user_taobao_feature[user][8] = -1
                self.user_taobao_feature[user][9] = -1
        
            # 16. total click nums
            self.user_taobao_feature[user][16] = self.user_action_nums[user][0]
        
            # 17. total buy nums
            self.user_taobao_feature[user][17] = self.user_action_nums[user][1]


if __name__ == '__main__':
    taobao_feature = taobao_user_feature()
    taobao_feature.get_taobao_user_feature()