# coding=utf-8

# 抽取口碑用户特征 54维度

class koubeiUserFeature():

    # 地点 6维
    locations_all = 0
    locations_7days = 0
    locations_15days = 0
    locations_first1month = 0
    locations_last1month = 0
    locations_last2month = 0

    # 时间 15维
    time_firsttime = 0
    time_lasttime = 0
    time_accounttime = 0
    time_longinterval = 0
    time_shortinterval = 0
    time_alldays = 0
    time_7days = 0
    time_15days = 0
    time_first1month = 0
    time_last1month = 0
    time_last2month = 0

    time_increasefromlast2tolast1month = 0
    time_increasefromfirst1tolast1month = 0
    time_daypermonth = 0.0
    time_period = 0.0

    # 商家 32维
    # 8
    merchants_all = 0
    merchants_7days = 0
    merchants_15days = 0
    merchants_first1month = 0
    merchants_last1month = 0
    merchants_last2month = 0
    merchants_increasefromlast2tolast1month = 0
    merchants_increasefromfirst1tolast1month = 0

    # 8
    merchantcounts_all = 0
    merchantcounts_7days = 0
    merchantcounts_15days = 0
    merchantcounts_first1month = 0
    merchantcounts_last1month = 0
    merchantcounts_last2month = 0
    merchantcounts_increasefromlast2tolast1month = 0
    merchantcounts_increasefromfirst1tolast1month = 0

    # 4
    merchants_1time = 0
    merchants_2time = 0
    merchants_3time = 0
    merchants_3plustime = 0

    # 6
    merchantcountsDivtime_alldays = 0.0
    merchantDivtime_alldays = 0.0
    merchants_1timeDivmerchants = 0.0
    merchants_2timeDivmerchants = 0.0
    merchants_3timeDivmerchants = 0.0
    merchants_3plustimeDivmerchants = 0.0

    # 6
    merchantcountsDivmerchants_all = 0.0
    merchantcountsDivmerchants_7days = 0.0
    merchantcountsDivmerchants_15days = 0.0
    merchantcountsDivmerchants_first1month = 0.0
    merchantcountsDivmerchants_last1month = 0.0
    merchantcountsDivmerchants_last2month = 0.0

    # 字典属性
    user_location = {}
    user_time = {}
    user_merchants = {}

    # 特征属性
    user_location_feature = {}
    user_time_feature = {}
    user_merchants_feature = {}
    koubei_user_feature = {}


    # 给定时间区间文件
    def getuserBasevalue(self, enddays):

        if enddays == 123:
            endmonth = 10
        if enddays == 153:
            endmonth = 11
        print 'Get the user base value..'
        file = '/home/wanghao/Document/tianchi/dataset/dataset_t/trainfrom7to%d_t'%(endmonth)
        with open(file, 'rb') as f :
            for line in f :
                line = line.strip('\r\n')
                user, merchant, location, time = line.split(',')
                time = int(time)
                # -------- location -----------
                if not self.user_location.has_key(user):
                    self.user_location[user] = {}
                    self.user_location[user]['all'] = []
                    self.user_location[user]['7'] = []
                    self.user_location[user]['15'] = []
                    self.user_location[user]['first1month'] = []
                    self.user_location[user]['last1month'] = []
                    self.user_location[user]['last2month'] = []

                if location not in self.user_location[user]['all']:
                    self.user_location[user]['all'].append(location)

                if time <= 31 :
                    if location not in self.user_location[user]['first1month'] :
                        self.user_location[user]['first1month'].append(location)

                if (time >= enddays - 31) and time < enddays:
                    if location not in self.user_location[user]['last1month']:
                        self.user_location[user]['last1month'].append(location)

                if (time >= enddays - 62) and time < enddays - 31:
                    if location not in self.user_location[user]['last2month']:
                        self.user_location[user]['last2month'].append(location)

                if (time >= enddays - 7) and time < enddays:
                    if location not in self.user_location[user]['7']:
                        self.user_location[user]['7'].append(location)

                if (time >= enddays - 15) and time < enddays:
                    if location not in self.user_location[user]['15']:
                        self.user_location[user]['15'].append(location)

                # ----- time -------------
                if not self.user_time.has_key(user):
                    self.user_time[user] = {}
                    self.user_time[user]['all'] = []
                    self.user_time[user]['7'] = []
                    self.user_time[user]['15'] = []
                    self.user_time[user]['first1month'] = []
                    self.user_time[user]['last1month'] = []
                    self.user_time[user]['last2month'] = []

                if time not in self.user_time[user]['all']:
                    self.user_time[user]['all'].append(time)

                if time <= 31:
                    if time not in self.user_time[user]['first1month']:
                        self.user_time[user]['first1month'].append(time)

                if (time >= enddays - 31) and time < enddays:
                    if time not in self.user_time[user]['last1month']:
                        self.user_time[user]['last1month'].append(time)

                if (time >= enddays - 62) and time < enddays - 31:
                    if time not in self.user_time[user]['last2month']:
                        self.user_time[user]['last2month'].append(time)

                if (time >= enddays - 7) and time < enddays:
                    if time not in self.user_time[user]['7']:
                        self.user_time[user]['7'].append(time)

                if (time >= enddays - 15) and time < enddays:
                    if time not in self.user_time[user]['15']:
                        self.user_time[user]['15'].append(time)


                # -----merchant ----------
                if not self.user_merchants.has_key(user):
                    self.user_merchants[user] = {}
                    self.user_merchants[user]['all'] = {}
                    self.user_merchants[user]['7'] = {}
                    self.user_merchants[user]['15'] = {}
                    self.user_merchants[user]['first1month'] = {}
                    self.user_merchants[user]['last1month'] = {}
                    self.user_merchants[user]['last2month'] = {}

                if not self.user_merchants[user]['all'].has_key(merchant):
                    self.user_merchants[user]['all'][merchant] = 0
                self.user_merchants[user]['all'][merchant] += 1

                if time <= 31:
                    if not self.user_merchants[user]['first1month'].has_key(merchant):
                        self.user_merchants[user]['first1month'][merchant] = 0
                    self.user_merchants[user]['first1month'][merchant] += 1

                if (time >= enddays - 31) and time < enddays:
                    if not self.user_merchants[user]['last1month'].has_key(merchant):
                        self.user_merchants[user]['last1month'][merchant] = 0
                    self.user_merchants[user]['last1month'][merchant] += 1

                if (time >= enddays - 62) and time < enddays - 31:
                    if not self.user_merchants[user]['last2month'].has_key(merchant):
                        self.user_merchants[user]['last2month'][merchant] = 0
                    self.user_merchants[user]['last2month'][merchant] += 1

                if (time >= enddays - 7) and time < enddays:
                    if not self.user_merchants[user]['7'].has_key(merchant):
                        self.user_merchants[user]['7'][merchant] = 0
                    self.user_merchants[user]['7'][merchant] += 1

                if (time >= enddays - 15) and time < enddays:
                    if not self.user_merchants[user]['15'].has_key(merchant):
                        self.user_merchants[user]['15'][merchant] = 0
                    self.user_merchants[user]['15'][merchant] += 1


    def getuserDivvalue(self, enddays):
        print 'Get the user div value ...'

        # -------- location -----------
        for user in self.user_location.keys():
            if not self.user_location_feature.has_key(user):
                self.user_location_feature[user] = [0]*6

            self.user_location_feature[user][0] = len(self.user_location[user]['all'])
            self.user_location_feature[user][1] = len(self.user_location[user]['7'])
            self.user_location_feature[user][2] = len(self.user_location[user]['15'])
            self.user_location_feature[user][3] = len(self.user_location[user]['first1month'])
            self.user_location_feature[user][4] = len(self.user_location[user]['last1month'])
            self.user_location_feature[user][5] = len(self.user_location[user]['last2month'])


        # -------- time -----------
        for user in self.user_time.keys():
            if not self.user_time_feature.has_key(user):
                self.user_time_feature[user] = [0] * 15

            self.user_time_feature[user][0] = min(self.user_time[user]['all'])
            self.user_time_feature[user][1] = max(self.user_time[user]['all'])
            self.user_time_feature[user][2] = enddays - min(self.user_time[user]['all'])

            if len(self.user_time[user]['all']) <= 1:
                self.user_time_feature[user][3] = -1
                self.user_time_feature[user][4] = -1
            else:
                sortedtime = sorted(self.user_time[user]['all'])
                maxtime = -1
                mintime = 100000
                for index in range(len(sortedtime)-1):
                    if (sortedtime[index + 1] - sortedtime[index]) > maxtime:
                        maxtime = sortedtime[index + 1] - sortedtime[index]
                    if (sortedtime[index + 1] - sortedtime[index]) < mintime:
                        mintime = sortedtime[index + 1] - sortedtime[index]
                self.user_time_feature[user][3] = maxtime
                self.user_time_feature[user][4] = mintime

            self.user_time_feature[user][5] = len(self.user_time[user]['all'])
            self.user_time_feature[user][6] = len(self.user_time[user]['7'])
            self.user_time_feature[user][7] = len(self.user_time[user]['15'])
            self.user_time_feature[user][8] = len(self.user_time[user]['first1month'])
            self.user_time_feature[user][9] = len(self.user_time[user]['last1month'])
            self.user_time_feature[user][10] = len(self.user_time[user]['last2month'])
            self.user_time_feature[user][11] = self.user_time_feature[user][11] - self.user_time_feature[user][12]
            self.user_time_feature[user][12] = self.user_time_feature[user][11] - self.user_time_feature[user][10]
            self.user_time_feature[user][13] = float(self.user_time_feature[user][5]) / (enddays/30)
            self.user_time_feature[user][14] = float(self.user_time_feature[user][1] - self.user_time_feature[user][0])/self.user_time_feature[user][5]

        # ---- merchant ----
        for user in self.user_merchants.keys():
            if not self.user_merchants_feature.has_key(user):
                self.user_merchants_feature[user] = [0] * 32

            self.user_merchants_feature[user][0] = len(self.user_merchants[user]['all'].keys())
            self.user_merchants_feature[user][1] = len(self.user_merchants[user]['7'].keys())
            self.user_merchants_feature[user][2] = len(self.user_merchants[user]['15'].keys())
            self.user_merchants_feature[user][3] = len(self.user_merchants[user]['first1month'].keys())
            self.user_merchants_feature[user][4] = len(self.user_merchants[user]['last1month'].keys())
            self.user_merchants_feature[user][5] = len(self.user_merchants[user]['last2month'].keys())
            self.user_merchants_feature[user][6] = self.user_merchants_feature[user][4] - self.user_merchants_feature[user][5]
            self.user_merchants_feature[user][7] = self.user_merchants_feature[user][4] - self.user_merchants_feature[user][3]

            count_all = 0
            for mer in self.user_merchants[user]['all'].keys():
                count_all = count_all + self.user_merchants[user]['all'][mer]
            self.user_merchants_feature[user][8] = count_all

            count_7days = 0
            for mer in self.user_merchants[user]['7'].keys():
                count_7days = count_7days + self.user_merchants[user]['7'][mer]
            self.user_merchants_feature[user][9] = count_7days

            count_15days = 0
            for mer in self.user_merchants[user]['15'].keys():
                count_15days = count_15days + self.user_merchants[user]['15'][mer]
            self.user_merchants_feature[user][10] = count_15days

            count_first1month = 0
            for mer in self.user_merchants[user]['first1month'].keys():
                count_first1month = count_first1month + self.user_merchants[user]['first1month'][mer]
            self.user_merchants_feature[user][11] = count_first1month

            count_last1month = 0
            for mer in self.user_merchants[user]['last1month'].keys():
                count_last1month = count_last1month + self.user_merchants[user]['last1month'][mer]
            self.user_merchants_feature[user][12] = count_last1month

            count_last2month = 0
            for mer in self.user_merchants[user]['last2month'].keys():
                count_last2month = count_last2month + self.user_merchants[user]['last2month'][mer]
            self.user_merchants_feature[user][13] = count_last2month

            self.user_merchants_feature[user][14] = self.user_merchants_feature[user][12] - self.user_merchants_feature[user][13]
            self.user_merchants_feature[user][15] = self.user_merchants_feature[user][12] - self.user_merchants_feature[user][11]

            merchant_count1 = 0
            merchant_count2 = 0
            merchant_count3 = 0
            merchant_count3plus = 0

            for mer in self.user_merchants[user]['all'].keys():
                if self.user_merchants[user]['all'][mer] == 1:
                    merchant_count1 += 1
                if self.user_merchants[user]['all'][mer] == 2:
                    merchant_count2 += 1
                if self.user_merchants[user]['all'][mer] == 3:
                    merchant_count3 += 1
                if self.user_merchants[user]['all'][mer] > 3:
                    merchant_count3plus += 1

            self.user_merchants_feature[user][16] = merchant_count1
            self.user_merchants_feature[user][17] = merchant_count2
            self.user_merchants_feature[user][18] = merchant_count3
            self.user_merchants_feature[user][19] = merchant_count3plus

            self.user_merchants_feature[user][20] = float(merchant_count1) / self.user_merchants_feature[user][0]
            self.user_merchants_feature[user][21] = float(merchant_count2) / self.user_merchants_feature[user][0]
            self.user_merchants_feature[user][22] = float(merchant_count3) / self.user_merchants_feature[user][0]
            self.user_merchants_feature[user][23] = float(merchant_count3plus) / self.user_merchants_feature[user][0]

            self.user_merchants_feature[user][24] = float(self.user_merchants_feature[user][8]) / self.user_time_feature[user][5]
            self.user_merchants_feature[user][25] = float(self.user_merchants_feature[user][0]) / self.user_time_feature[user][5]

            self.user_merchants_feature[user][26] = float(self.user_merchants_feature[user][8]) / self.user_merchants_feature[user][0]
            if self.user_merchants_feature[user][1] == 0 :
                self.user_merchants_feature[user][27] = 0
            else:
                self.user_merchants_feature[user][27] = float(self.user_merchants_feature[user][9]) / self.user_merchants_feature[user][1]

            if self.user_merchants_feature[user][2] == 0 :
                self.user_merchants_feature[user][28] = 0
            else:
                self.user_merchants_feature[user][28] = float(self.user_merchants_feature[user][10]) / self.user_merchants_feature[user][2]

            if self.user_merchants_feature[user][3] == 0:
                self.user_merchants_feature[user][29] = 0
            else:
                self.user_merchants_feature[user][29] = float(self.user_merchants_feature[user][11]) / self.user_merchants_feature[user][3]

            if self.user_merchants_feature[user][4] == 0 :
                self.user_merchants_feature[user][30] = 0
            else:
                self.user_merchants_feature[user][30] = float(self.user_merchants_feature[user][12]) / self.user_merchants_feature[user][4]

            if self.user_merchants_feature[user][5] == 0 :
                self.user_merchants_feature[user][31] = 0
            else:
                self.user_merchants_feature[user][31] = float(self.user_merchants_feature[user][13]) / self.user_merchants_feature[user][5]



    # ----  汇总用户特征
    def mergeuserFeature(self, enddays):

        self.getuserBasevalue(enddays)
        self.getuserDivvalue(enddays)
        print 'merge koubei user feature ....'
        for user in self.user_merchants_feature.keys():
            if not self.koubei_user_feature.has_key(user):
                self.koubei_user_feature[user] = []
            self.koubei_user_feature[user].extend(self.user_location_feature[user])
            self.koubei_user_feature[user].extend(self.user_time_feature[user])
            self.koubei_user_feature[user].extend(self.user_merchants_feature[user])

if __name__ == '__main__':

    kb = koubeiUserFeature()
    kb.mergeuserFeature(153)
    for user in kb.koubei_user_feature.keys():
        print kb.koubei_user_feature[user]
