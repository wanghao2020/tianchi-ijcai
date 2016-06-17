# coding=utf-8

# 抽取口碑用户和商家特征

class koubeiUserMerchantFeature():

    # (user, merchant)

    # time

    # count

    # days

    # ratio


    User_Merchant_count = {}
    User_Merchant_numbers = {}
    User_merchant_frequency = {}
    User_Merchant_days = {}

    UserAndMerchant_time = {}
    UserAndMerchant_count = {}
    UserAndMerchant_locations = {}

    UserAndMerchant_time_feature = {}
    UserAndMerchant_feature = {}

    UserAndMerchantFeature = {}


    # 统计用户相关信息
    def getUservalue(self, enddays):

        if enddays == 123:
            endmonth = 10
        if enddays == 153:
            endmonth = 11
        file = '/home/wanghao/Document/tianchi/dataset/dataset_t/trainfrom7to%d_t' % (endmonth)
        print 'Get the user merchant count ...'
        with open(file, 'rb') as f :
            for line in f :
                line = line.strip('\r\n')
                user, merchant, location, time = line.split(',')

                # 用户总的所去商家数
                if not self.User_Merchant_count.has_key(user):
                    self.User_Merchant_count[user] = {}
                    self.User_Merchant_count[user]['all'] = {}
                    self.User_Merchant_count[user]['7'] = {}
                    self.User_Merchant_count[user]['15'] = {}
                    self.User_Merchant_count[user]['first1month'] = {}
                    self.User_Merchant_count[user]['last1month'] = {}
                    self.User_Merchant_count[user]['last2month'] = {}

                if not self.User_Merchant_count[user]['all'].has_key(merchant):
                    self.User_Merchant_count[user]['all'][merchant] = 0
                self.User_Merchant_count[user]['all'][merchant] += 1

                if time <= 31:
                    if not self.User_Merchant_count[user]['first1month'].has_key(merchant):
                        self.User_Merchant_count[user]['first1month'][merchant] = 0
                    self.User_Merchant_count[user]['first1month'][merchant] += 1

                if (time >= enddays - 31) and time < enddays:
                    if not self.User_Merchant_count[user]['last1month'].has_key(merchant):
                        self.User_Merchant_count[user]['last1month'][merchant] = 0
                    self.User_Merchant_count[user]['last1month'][merchant] += 1

                if (time >= enddays - 62) and time < enddays - 31:
                    if not self.User_Merchant_count[user]['last2month'].has_key(merchant):
                        self.User_Merchant_count[user]['last2month'][merchant] = 0
                    self.User_Merchant_count[user]['last2month'][merchant] += 1

                if (time >= enddays - 7) and time < enddays:
                    if not self.User_Merchant_count[user]['7'].has_key(merchant):
                        self.User_Merchant_count[user]['7'][merchant] = 0
                    self.User_Merchant_count[user]['7'][merchant] += 1

                if (time >= enddays - 15) and time < enddays:
                    if not self.User_Merchant_count[user]['15'].has_key(merchant):
                        self.User_Merchant_count[user]['15'][merchant] = 0
                    self.User_Merchant_count[user]['15'][merchant] += 1


                # 用户总的活跃天数
                if not self.User_Merchant_days.has_key(user):
                    self.User_Merchant_days[user] = {}
                    self.User_Merchant_days[user]['all'] = []
                    self.User_Merchant_days[user]['7'] = []
                    self.User_Merchant_days[user]['15'] = []
                    self.User_Merchant_days[user]['first1month'] = []
                    self.User_Merchant_days[user]['last1month'] = []
                    self.User_Merchant_days[user]['last2month'] = []

                if time not in self.User_Merchant_days[user]['all']:
                    self.User_Merchant_days[user]['all'].append(time)

                if time <= 31:
                    if time not in self.User_Merchant_days[user]['first1month']:
                        self.User_Merchant_days[user]['first1month'].append(time)

                if (time >= enddays - 31) and time < enddays:
                    if time not in self.User_Merchant_days[user]['last1month']:
                        self.User_Merchant_days[user]['last1month'].append(time)

                if (time >= enddays - 62) and time < enddays - 31:
                    if time not in self.User_Merchant_days[user]['last2month']:
                        self.User_Merchant_days[user]['last2month'].append(time)

                if (time >= enddays - 7) and time < enddays:
                    if time not in self.User_Merchant_days[user]['7']:
                        self.User_Merchant_days[user]['7'].append(time)

                if (time >= enddays - 15) and time < enddays:
                    if time not in self.User_Merchant_days[user]['15']:
                        self.User_Merchant_days[user]['15'].append(time)


                # 用户所去商家的地点数: (用户，商家) : [地点1，地点2 ...]
                if not self.UserAndMerchant_locations.has_key((user,merchant)):
                    self.UserAndMerchant_locations[(user,merchant)] = []
                if location not in self.UserAndMerchant_locations[(user, merchant)]:
                    self.UserAndMerchant_locations[(user,merchant)].append(location)


        for user in self.User_Merchant_count.keys():
            # 统计用户所去商家的个数
            if not self.User_Merchant_numbers.has_key(user):
                self.User_Merchant_numbers[user] = {}
                self.User_Merchant_numbers[user]['all'] = len(self.User_Merchant_count[user]['all'].keys())
                self.User_Merchant_numbers[user]['7'] = len(self.User_Merchant_count[user]['7'].keys())
                self.User_Merchant_numbers[user]['15'] = len(self.User_Merchant_count[user]['15'].keys())
                self.User_Merchant_numbers[user]['first1month'] = len(self.User_Merchant_count[user]['first1month'].keys())
                self.User_Merchant_numbers[user]['last1month'] = len(self.User_Merchant_count[user]['last1month'].keys())
                self.User_Merchant_numbers[user]['last2month'] = len(self.User_Merchant_count[user]['last2month'].keys())

            # 统计用户所去商家的次数
            if not self.User_merchant_frequency.has_key(user):
                self.User_merchant_frequency[user] = {}

                count_all = 0
                for mer in self.User_Merchant_count[user]['all'].keys():
                    count_all = count_all + self.User_Merchant_count[user]['all'][mer]

                count_7days = 0
                for mer in self.User_Merchant_count[user]['7'].keys():
                    count_7days = count_7days + self.User_Merchant_count[user]['7'][mer]

                count_15days = 0
                for mer in self.User_Merchant_count[user]['15'].keys():
                    count_15days = count_15days + self.User_Merchant_count[user]['15'][mer]

                count_first1month = 0
                for mer in self.User_Merchant_count[user]['first1month'].keys():
                    count_first1month = count_first1month + self.User_Merchant_count[user]['first1month'][mer]

                count_last1month = 0
                for mer in self.User_Merchant_count[user]['last1month'].keys():
                    count_last1month = count_last1month + self.User_Merchant_count[user]['last1month'][mer]

                count_last2month = 0
                for mer in self.User_Merchant_count[user]['last2month'].keys():
                    count_last2month = count_last2month + self.User_Merchant_count[user]['last2month'][mer]

                self.User_merchant_frequency[user]['all'] = count_all
                self.User_merchant_frequency[user]['7'] = count_7days
                self.User_merchant_frequency[user]['15'] = count_15days
                self.User_merchant_frequency[user]['first1month'] = count_first1month
                self.User_merchant_frequency[user]['last1month'] = count_last1month
                self.User_merchant_frequency[user]['last2month'] = count_last2month


    def getUserAndMerchantBasevalue(self, enddays):

        if enddays == 123:
            endmonth = 10
        if enddays == 153:
            endmonth = 11
        file = '/home/wanghao/Document/tianchi/dataset/dataset_t/trainfrom7to%d_t' % (endmonth)
        print 'Get the user merchant base value ...'
        with open(file, 'rb') as f :
            for line in f :
                line = line.strip('\r\n')
                user, merchant, location, time = line.split(',')
                time = int(time)

                # ---- user and merchant time
                if not self.UserAndMerchant_time.has_key((user,merchant)):
                    self.UserAndMerchant_time[(user, merchant)] = []
                if time not in self.UserAndMerchant_time[(user, merchant)]:
                    self.UserAndMerchant_time[(user, merchant)].append(time)

                # ---- user and merchant frequency
                if not self.UserAndMerchant_count.has_key((user,merchant)):
                    self.UserAndMerchant_count[(user,merchant)] = {}
                    self.UserAndMerchant_count[(user,merchant)]['all'] = []
                    self.UserAndMerchant_count[(user,merchant)]['7'] = []
                    self.UserAndMerchant_count[(user,merchant)]['15'] = []
                    self.UserAndMerchant_count[(user,merchant)]['first1month'] = []
                    self.UserAndMerchant_count[(user,merchant)]['last1month'] = []
                    self.UserAndMerchant_count[(user,merchant)]['last2month'] = []

                self.UserAndMerchant_count[(user,merchant)]['all'].append(time)

                if time <= 31:
                    self.UserAndMerchant_count[(user,merchant)]['first1month'].append(time)

                if (time >= enddays - 31) and time < enddays:
                    self.UserAndMerchant_count[(user, merchant)]['last1month'].append(time)

                if (time >= enddays - 62) and time < enddays - 31:
                    self.UserAndMerchant_count[(user, merchant)]['last2month'].append(time)

                if (time >= enddays - 7) and time < enddays:
                    self.UserAndMerchant_count[(user, merchant)]['7'].append(time)

                if (time >= enddays - 15) and time < enddays:
                    self.UserAndMerchant_count[(user, merchant)]['15'].append(time)


    def getUserAndMerchantDivvalue(self, enddays):

        print 'Get the user and merchant div value ...'

        for key in self.UserAndMerchant_time.keys():

            # 交互时间统计
            if not self.UserAndMerchant_time_feature.has_key(key):
                self.UserAndMerchant_time_feature[key] = [0] * 6

            self.UserAndMerchant_time_feature[key][0] = min(self.UserAndMerchant_time[key])
            self.UserAndMerchant_time_feature[key][1] = max(self.UserAndMerchant_time[key])

            if len(self.UserAndMerchant_time[key]) <= 1:
                self.UserAndMerchant_time_feature[key][2] = -1
                self.UserAndMerchant_time_feature[key][3] = -1
                self.UserAndMerchant_time_feature[key][4] = -1
            else:
                sortedtime = sorted(self.UserAndMerchant_time[key])
                maxtime = -1
                mintime = 100000
                alltime = 0
                for index in range(len(sortedtime) - 1):
                    if (sortedtime[index + 1] - sortedtime[index]) > maxtime:
                        maxtime = sortedtime[index + 1] - sortedtime[index]
                    if (sortedtime[index + 1] - sortedtime[index]) < mintime:
                        mintime = sortedtime[index + 1] - sortedtime[index]
                    alltime = alltime + sortedtime[index + 1] - sortedtime[index]
                self.UserAndMerchant_time_feature[key][2] = maxtime
                self.UserAndMerchant_time_feature[key][3] = mintime
                self.UserAndMerchant_time_feature[key][4] = float(alltime) / (len(sortedtime) - 1)

            self.UserAndMerchant_time_feature[key][5] = self.UserAndMerchant_time_feature[key][1] - self.UserAndMerchant_time_feature[key][0]


            # 次数，天数统计
            if not self.UserAndMerchant_feature.has_key(key):
                self.UserAndMerchant_feature[key] = [0] * 42

            # 次数
            self.UserAndMerchant_feature[key][0] = len(self.UserAndMerchant_count[key]['all'])
            self.UserAndMerchant_feature[key][1] = len(self.UserAndMerchant_count[key]['7'])
            self.UserAndMerchant_feature[key][2] = len(self.UserAndMerchant_count[key]['15'])
            self.UserAndMerchant_feature[key][3] = len(self.UserAndMerchant_count[key]['first1month'])
            self.UserAndMerchant_feature[key][4] = len(self.UserAndMerchant_count[key]['last1month'])
            self.UserAndMerchant_feature[key][5] = len(self.UserAndMerchant_count[key]['last2month'])
            self.UserAndMerchant_feature[key][6] = float(self.UserAndMerchant_feature[key][0]) / (enddays/30)
            self.UserAndMerchant_feature[key][7] = self.UserAndMerchant_feature[key][4] - self.UserAndMerchant_feature[key][5]
            self.UserAndMerchant_feature[key][8] = self.UserAndMerchant_feature[key][4] - self.UserAndMerchant_feature[key][3]

            # 天数
            self.UserAndMerchant_feature[key][9] = len(set(self.UserAndMerchant_count[key]['all']))
            self.UserAndMerchant_feature[key][10] = len(set(self.UserAndMerchant_count[key]['7']))
            self.UserAndMerchant_feature[key][11] = len(set(self.UserAndMerchant_count[key]['15']))
            self.UserAndMerchant_feature[key][12] = len(set(self.UserAndMerchant_count[key]['first1month']))
            self.UserAndMerchant_feature[key][13] = len(set(self.UserAndMerchant_count[key]['last1month']))
            self.UserAndMerchant_feature[key][14] = len(set(self.UserAndMerchant_count[key]['last2month']))
            self.UserAndMerchant_feature[key][15] = float(self.UserAndMerchant_feature[key][9]) / (enddays / 30)
            self.UserAndMerchant_feature[key][16] = self.UserAndMerchant_feature[key][13] - self.UserAndMerchant_feature[key][14]
            self.UserAndMerchant_feature[key][17] = self.UserAndMerchant_feature[key][13] - self.UserAndMerchant_feature[key][12]

            # 去该商家的次数 / 用户去所有商家的次数
            if self.User_merchant_frequency[key[0]]['all'] == 0 :
                self.UserAndMerchant_feature[key][18] = 0
            else :
                self.UserAndMerchant_feature[key][18] = float(self.UserAndMerchant_feature[key][0]) / self.User_merchant_frequency[key[0]]['all']

            if self.User_merchant_frequency[key[0]]['7'] == 0:
                self.UserAndMerchant_feature[key][19] = 0
            else:
                self.UserAndMerchant_feature[key][19] = float(self.UserAndMerchant_feature[key][1]) / self.User_merchant_frequency[key[0]]['7']

            if self.User_merchant_frequency[key[0]]['15'] == 0 :
                self.UserAndMerchant_feature[key][20] = 0
            else:
                self.UserAndMerchant_feature[key][20] = float(self.UserAndMerchant_feature[key][2]) / self.User_merchant_frequency[key[0]]['15']

            if self.User_merchant_frequency[key[0]]['first1month'] == 0 :
                self.UserAndMerchant_feature[key][21] = 0
            else:
                self.UserAndMerchant_feature[key][21] = float(self.UserAndMerchant_feature[key][3]) / self.User_merchant_frequency[key[0]]['first1month']

            if self.User_merchant_frequency[key[0]]['last1month'] == 0:
                self.UserAndMerchant_feature[key][22] = 0
            else:
                self.UserAndMerchant_feature[key][22] = float(self.UserAndMerchant_feature[key][4]) / self.User_merchant_frequency[key[0]]['last1month']

            if self.User_merchant_frequency[key[0]]['last2month'] == 0 :
                self.UserAndMerchant_feature[key][23] = 0
            else :
                self.UserAndMerchant_feature[key][23] = float(self.UserAndMerchant_feature[key][5]) / self.User_merchant_frequency[key[0]]['last2month']
            self.UserAndMerchant_feature[key][24] = self.UserAndMerchant_feature[key][22] - self.UserAndMerchant_feature[key][23]
            self.UserAndMerchant_feature[key][25] = self.UserAndMerchant_feature[key][22] - self.UserAndMerchant_feature[key][21]



            # 去该商家的天数 / 用户的活跃天数
            if len(self.User_Merchant_days[key[0]]['all']) == 0 :
                self.UserAndMerchant_feature[key][26] = 0
            else :
                self.UserAndMerchant_feature[key][26] = float(self.UserAndMerchant_feature[key][9]) / len(self.User_Merchant_days[key[0]]['all'])

            if len(self.User_Merchant_days[key[0]]['7']) == 0:
                self.UserAndMerchant_feature[key][27] = 0
            else:
                self.UserAndMerchant_feature[key][27] = float(self.UserAndMerchant_feature[key][10]) / len(self.User_Merchant_days[key[0]]['7'])

            if len(self.User_Merchant_days[key[0]]['15']) == 0:
                self.UserAndMerchant_feature[key][28] = 0
            else:
                self.UserAndMerchant_feature[key][28] = float(self.UserAndMerchant_feature[key][11]) / len(self.User_Merchant_days[key[0]]['15'])

            if len(self.User_Merchant_days[key[0]]['first1month']) == 0 :
                self.UserAndMerchant_feature[key][29] = 0
            else :
                self.UserAndMerchant_feature[key][29] = float(self.UserAndMerchant_feature[key][12]) / len(self.User_Merchant_days[key[0]]['first1month'])

            if len(self.User_Merchant_days[key[0]]['last1month']) == 0:
                self.UserAndMerchant_feature[key][30] = 0
            else:
                self.UserAndMerchant_feature[key][30] = float(self.UserAndMerchant_feature[key][13]) / len(self.User_Merchant_days[key[0]]['last1month'])

            if len(self.User_Merchant_days[key[0]]['last2month']) == 0 :
                self.UserAndMerchant_feature[key][31] = 0
            else:
                self.UserAndMerchant_feature[key][31] = float(self.UserAndMerchant_feature[key][14]) /  len(self.User_Merchant_days[key[0]]['last2month'])

            self.UserAndMerchant_feature[key][32] = self.UserAndMerchant_feature[key][30] - self.UserAndMerchant_feature[key][31]
            self.UserAndMerchant_feature[key][33] = self.UserAndMerchant_feature[key][30] - self.UserAndMerchant_feature[key][29]

            # 去该商家的次数 / 用户的活跃天数
            if len(self.User_Merchant_days[key[0]]['all']) == 0 :
                self.UserAndMerchant_feature[key][34] = 0
            else:
              self.UserAndMerchant_feature[key][34] = float(self.UserAndMerchant_feature[key][0]) / len(self.User_Merchant_days[key[0]]['all'])

            if len(self.User_Merchant_days[key[0]]['7']) == 0 :
                self.UserAndMerchant_feature[key][35] = 0
            else:
                self.UserAndMerchant_feature[key][35] = float(self.UserAndMerchant_feature[key][1]) / len(self.User_Merchant_days[key[0]]['7'])

            if len(self.User_Merchant_days[key[0]]['15']) == 0:
                self.UserAndMerchant_feature[key][36] = 0
            else:
                self.UserAndMerchant_feature[key][36] = float(self.UserAndMerchant_feature[key][2]) / len(self.User_Merchant_days[key[0]]['15'])

            if len(self.User_Merchant_days[key[0]]['first1month']) == 0 :
                self.UserAndMerchant_feature[key][37] = 0
            else:
                self.UserAndMerchant_feature[key][37] = float(self.UserAndMerchant_feature[key][3]) / len(self.User_Merchant_days[key[0]]['first1month'])

            if len(self.User_Merchant_days[key[0]]['last1month']) == 0 :
                self.UserAndMerchant_feature[key][38] = 0
            else:
                self.UserAndMerchant_feature[key][38] = float(self.UserAndMerchant_feature[key][4]) / len(self.User_Merchant_days[key[0]]['last1month'])

            if len(self.User_Merchant_days[key[0]]['last2month']) == 0 :
                self.UserAndMerchant_feature[key][39] = 0
            else:
                self.UserAndMerchant_feature[key][39] = float(self.UserAndMerchant_feature[key][3]) / len(self.User_Merchant_days[key[0]]['last2month'])

            self.UserAndMerchant_feature[key][40] = self.UserAndMerchant_feature[key][38] - self.UserAndMerchant_feature[key][39]
            self.UserAndMerchant_feature[key][41] = self.UserAndMerchant_feature[key][38] - self.UserAndMerchant_feature[key][37]


    def mergeUserandMerchantFeature(self, enddays):


        self.getUservalue(enddays)
        self.getUserAndMerchantBasevalue(enddays)
        self.getUserAndMerchantDivvalue(enddays)

        print 'Merge the user and merchant feature ...'

        # (user, merchant)
        for key in self.UserAndMerchant_time_feature.keys():
            if not self.UserAndMerchantFeature.has_key(key):
                self.UserAndMerchantFeature[key] = []
            self.UserAndMerchantFeature[key].append(len(self.UserAndMerchant_locations[key]))
            self.UserAndMerchantFeature[key].extend(self.UserAndMerchant_time_feature[key])
            self.UserAndMerchantFeature[key].extend(self.UserAndMerchant_feature[key])



if __name__ == '__main__':

    kb = koubeiUserMerchantFeature()
    kb.mergeUserandMerchantFeature(153)
    for key in kb.UserAndMerchantFeature.keys():
        print key,'  :   ',kb.UserAndMerchantFeature[key]
    print 'the size :', len(kb.UserAndMerchantFeature.keys())