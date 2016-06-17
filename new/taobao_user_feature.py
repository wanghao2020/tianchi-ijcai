# coding=utf-8

# 抽取淘宝用户特征

class taobaoUserFeature():


    user_days = {}
    user_buydays = {}

    user_buyitems = {}
    user_clickitems = {}
    user_buycategory = {}
    user_clickcategory = {}
    user_buyseller = {}
    user_clickseller = {}

    user_time_feature = {}
    user_buyandclick_feature = {}

    taobao_userFeature = {}

    def getTaobaoUserBasevalue(self, enddays):

        if enddays == 123:
            endmonth = 10
        if enddays == 153:
            endmonth = 11
        file = '/home/wanghao/Document/tianchi/dataset/dataset_t/taobaofrom7to%d_t' %(endmonth)
        print 'Get the taobao user base value ...'

        with open(file, 'rb') as f :
            for line in f :
                line = line.strip('\r\n')
                user, seller, item, category, action, time = line.split(',')
                action = int(action)
                time = int(time)

                # 活跃天数
                if not self.user_days.has_key(user):
                    self.user_days[user] = []
                if time not in self.user_days[user]:
                    self.user_days[user].append(time)

                # 购物天数
                if action == 1:
                    if not self.user_buydays.has_key(user):
                        self.user_buydays[user] = []
                    if time not in self.user_buydays[user]:
                        self.user_buydays[user].append(time)

                # 点击物品次数
                if action == 0 :
                    if not self.user_clickitems.has_key(user):
                        self.user_clickitems[user] = {}
                        self.user_clickitems[user]['all'] = {}
                        self.user_clickitems[user]['7'] = {}
                        self.user_clickitems[user]['15'] = {}
                        self.user_clickitems[user]['first1month'] = {}
                        self.user_clickitems[user]['last1month'] = {}
                        self.user_clickitems[user]['last2month'] = {}

                    if not self.user_clickitems[user]['all'].has_key(item):
                        self.user_clickitems[user]['all'][item] = 0
                    self.user_clickitems[user]['all'][item] += 1

                    if time <= 31:
                        if not self.user_clickitems[user]['first1month'].has_key(item):
                            self.user_clickitems[user]['first1month'][item] = 0
                        self.user_clickitems[user]['first1month'][item] += 1

                    if (time >= enddays - 31) and time < enddays:
                        if not self.user_clickitems[user]['last1month'].has_key(item):
                            self.user_clickitems[user]['last1month'][item] = 0
                        self.user_clickitems[user]['last1month'][item] += 1

                    if (time >= enddays - 62) and time < enddays - 31:
                        if not self.user_clickitems[user]['last2month'].has_key(item):
                            self.user_clickitems[user]['last2month'][item] = 0
                        self.user_clickitems[user]['last2month'][item] += 1

                    if (time >= enddays - 7) and time < enddays:
                        if not self.user_clickitems[user]['7'].has_key(item):
                            self.user_clickitems[user]['7'][item] = 0
                        self.user_clickitems[user]['7'][item] += 1

                    if (time >= enddays - 15) and time < enddays:
                        if not self.user_clickitems[user]['15'].has_key(item):
                            self.user_clickitems[user]['15'][item] = 0
                        self.user_clickitems[user]['15'][item] += 1

                # 购买物品的次数
                if action == 1:
                    if not self.user_buyitems.has_key(user):
                        self.user_buyitems[user] = {}
                        self.user_buyitems[user]['all'] = {}
                        self.user_buyitems[user]['7'] = {}
                        self.user_buyitems[user]['15'] = {}
                        self.user_buyitems[user]['first1month'] = {}
                        self.user_buyitems[user]['last1month'] = {}
                        self.user_buyitems[user]['last2month'] = {}

                    if not self.user_buyitems[user]['all'].has_key(item):
                        self.user_buyitems[user]['all'][item] = 0
                    self.user_buyitems[user]['all'][item] += 1

                    if time <= 31:
                        if not self.user_buyitems[user]['first1month'].has_key(item):
                            self.user_buyitems[user]['first1month'][item] = 0
                        self.user_buyitems[user]['first1month'][item] += 1

                    if (time >= enddays - 31) and time < enddays:
                        if not self.user_buyitems[user]['last1month'].has_key(item):
                            self.user_buyitems[user]['last1month'][item] = 0
                        self.user_buyitems[user]['last1month'][item] += 1

                    if (time >= enddays - 62) and time < enddays - 31:
                        if not self.user_buyitems[user]['last2month'].has_key(item):
                            self.user_buyitems[user]['last2month'][item] = 0
                        self.user_buyitems[user]['last2month'][item] += 1

                    if (time >= enddays - 7) and time < enddays:
                        if not self.user_buyitems[user]['7'].has_key(item):
                            self.user_buyitems[user]['7'][item] = 0
                        self.user_buyitems[user]['7'][item] += 1

                    if (time >= enddays - 15) and time < enddays:
                        if not self.user_buyitems[user]['15'].has_key(item):
                            self.user_buyitems[user]['15'][item] = 0
                        self.user_buyitems[user]['15'][item] += 1

                # 点击类别的次数
                if action == 0:
                    if not self.user_clickcategory.has_key(user):
                        self.user_clickcategory[user] = {}
                        self.user_clickcategory[user]['all'] = {}
                        self.user_clickcategory[user]['7'] = {}
                        self.user_clickcategory[user]['15'] = {}
                        self.user_clickcategory[user]['first1month'] = {}
                        self.user_clickcategory[user]['last1month'] = {}
                        self.user_clickcategory[user]['last2month'] = {}

                    if not self.user_clickcategory[user]['all'].has_key(category):
                        self.user_clickcategory[user]['all'][category] = 0
                    self.user_clickcategory[user]['all'][category] += 1

                    if time <= 31:
                        if not self.user_clickcategory[user]['first1month'].has_key(category):
                            self.user_clickcategory[user]['first1month'][category] = 0
                        self.user_clickcategory[user]['first1month'][category] += 1

                    if (time >= enddays - 31) and time < enddays:
                        if not self.user_clickcategory[user]['last1month'].has_key(category):
                            self.user_clickcategory[user]['last1month'][category] = 0
                        self.user_clickcategory[user]['last1month'][category] += 1

                    if (time >= enddays - 62) and time < enddays - 31:
                        if not self.user_clickcategory[user]['last2month'].has_key(category):
                            self.user_clickcategory[user]['last2month'][category] = 0
                        self.user_clickcategory[user]['last2month'][category] += 1

                    if (time >= enddays - 7) and time < enddays:
                        if not self.user_clickcategory[user]['7'].has_key(category):
                            self.user_clickcategory[user]['7'][category] = 0
                        self.user_clickcategory[user]['7'][category] += 1

                    if (time >= enddays - 15) and time < enddays:
                        if not self.user_clickcategory[user]['15'].has_key(category):
                            self.user_clickcategory[user]['15'][category] = 0
                        self.user_clickcategory[user]['15'][category] += 1

                # 购买类别的次数
                if action == 1:
                    if not self.user_buycategory.has_key(user):
                        self.user_buycategory[user] = {}
                        self.user_buycategory[user]['all'] = {}
                        self.user_buycategory[user]['7'] = {}
                        self.user_buycategory[user]['15'] = {}
                        self.user_buycategory[user]['first1month'] = {}
                        self.user_buycategory[user]['last1month'] = {}
                        self.user_buycategory[user]['last2month'] = {}

                    if not self.user_buycategory[user]['all'].has_key(category):
                        self.user_buycategory[user]['all'][category] = 0
                    self.user_buycategory[user]['all'][category] += 1

                    if time <= 31:
                        if not self.user_buycategory[user]['first1month'].has_key(category):
                            self.user_buycategory[user]['first1month'][category] = 0
                        self.user_buycategory[user]['first1month'][category] += 1

                    if (time >= enddays - 31) and time < enddays:
                        if not self.user_buycategory[user]['last1month'].has_key(category):
                            self.user_buycategory[user]['last1month'][category] = 0
                        self.user_buycategory[user]['last1month'][category] += 1

                    if (time >= enddays - 62) and time < enddays - 31:
                        if not self.user_buycategory[user]['last2month'].has_key(category):
                            self.user_buycategory[user]['last2month'][category] = 0
                        self.user_buycategory[user]['last2month'][category] += 1

                    if (time >= enddays - 7) and time < enddays:
                        if not self.user_buycategory[user]['7'].has_key(category):
                            self.user_buycategory[user]['7'][category] = 0
                        self.user_buycategory[user]['7'][category] += 1

                    if (time >= enddays - 15) and time < enddays:
                        if not self.user_buycategory[user]['15'].has_key(category):
                            self.user_buycategory[user]['15'][category] = 0
                        self.user_buycategory[user]['15'][category] += 1

                # 点击商家的个数
                if action == 0:
                    if not self.user_clickseller.has_key(user):
                        self.user_clickseller[user] = {}
                        self.user_clickseller[user]['all'] = {}
                        self.user_clickseller[user]['7'] = {}
                        self.user_clickseller[user]['15'] = {}
                        self.user_clickseller[user]['first1month'] = {}
                        self.user_clickseller[user]['last1month'] = {}
                        self.user_clickseller[user]['last2month'] = {}

                    if not self.user_clickseller[user]['all'].has_key(seller):
                        self.user_clickseller[user]['all'][seller] = 0
                    self.user_clickseller[user]['all'][seller] += 1

                    if time <= 31:
                        if not self.user_clickseller[user]['first1month'].has_key(seller):
                            self.user_clickseller[user]['first1month'][seller] = 0
                        self.user_clickseller[user]['first1month'][seller] += 1

                    if (time >= enddays - 31) and time < enddays:
                        if not self.user_clickseller[user]['last1month'].has_key(seller):
                            self.user_clickseller[user]['last1month'][seller] = 0
                        self.user_clickseller[user]['last1month'][seller] += 1

                    if (time >= enddays - 62) and time < enddays - 31:
                        if not self.user_clickseller[user]['last2month'].has_key(seller):
                            self.user_clickseller[user]['last2month'][seller] = 0
                        self.user_clickseller[user]['last2month'][seller] += 1

                    if (time >= enddays - 7) and time < enddays:
                        if not self.user_clickseller[user]['7'].has_key(seller):
                            self.user_clickseller[user]['7'][seller] = 0
                        self.user_clickseller[user]['7'][seller] += 1

                    if (time >= enddays - 15) and time < enddays:
                        if not self.user_clickseller[user]['15'].has_key(seller):
                            self.user_clickseller[user]['15'][seller] = 0
                        self.user_clickseller[user]['15'][seller] += 1

                # 购买商家的个数
                if action == 1:
                    if not self.user_buyseller.has_key(user):
                        self.user_buyseller[user] = {}
                        self.user_buyseller[user]['all'] = {}
                        self.user_buyseller[user]['7'] = {}
                        self.user_buyseller[user]['15'] = {}
                        self.user_buyseller[user]['first1month'] = {}
                        self.user_buyseller[user]['last1month'] = {}
                        self.user_buyseller[user]['last2month'] = {}

                    if not self.user_buyseller[user]['all'].has_key(seller):
                        self.user_buyseller[user]['all'][seller] = 0
                    self.user_buyseller[user]['all'][seller] += 1

                    if time <= 31:
                        if not self.user_buyseller[user]['first1month'].has_key(seller):
                            self.user_buyseller[user]['first1month'][seller] = 0
                        self.user_buyseller[user]['first1month'][seller] += 1

                    if (time >= enddays - 31) and time < enddays:
                        if not self.user_buyseller[user]['last1month'].has_key(seller):
                            self.user_buyseller[user]['last1month'][seller] = 0
                        self.user_buyseller[user]['last1month'][seller] += 1

                    if (time >= enddays - 62) and time < enddays - 31:
                        if not self.user_buyseller[user]['last2month'].has_key(seller):
                            self.user_buyseller[user]['last2month'][seller] = 0
                        self.user_buyseller[user]['last2month'][seller] += 1

                    if (time >= enddays - 7) and time < enddays:
                        if not self.user_buyseller[user]['7'].has_key(seller):
                            self.user_buyseller[user]['7'][seller] = 0
                        self.user_buyseller[user]['7'][seller] += 1

                    if (time >= enddays - 15) and time < enddays:
                        if not self.user_buyseller[user]['15'].has_key(seller):
                            self.user_buyseller[user]['15'][seller] = 0
                        self.user_buyseller[user]['15'][seller] += 1


    def getTaobaoDivvalue(self, enddays):

        print 'Get the taobao user div value ...'
        for user in self.user_days.keys():

            # taobao user time feature
            if not self.user_time_feature.has_key(user):
                self.user_time_feature[user] = [0] * 12

            # 购物天数
            if not self.user_buydays.has_key(user):
                self.user_time_feature[user][0] = 0
                self.user_time_feature[user][1] = 0
                self.user_time_feature[user][2] = 0
                self.user_time_feature[user][3] = -1
                self.user_time_feature[user][4] = -1
            else:
                self.user_time_feature[user][0] = min(self.user_buydays[user])
                self.user_time_feature[user][1] = max(self.user_buydays[user])
                self.user_time_feature[user][2] = len(self.user_buydays[user])
                if len(self.user_buydays[user]) <= 1:
                    self.user_time_feature[user][3] = -1
                    self.user_time_feature[user][4] = -1
                else:
                    sortedtime = sorted(self.user_buydays[user])
                    maxtime = -1
                    mintime = 100000
                    for index in range(len(sortedtime) - 1):
                        if (sortedtime[index + 1] - sortedtime[index]) > maxtime:
                            maxtime = sortedtime[index + 1] - sortedtime[index]
                        if (sortedtime[index + 1] - sortedtime[index]) < mintime:
                            mintime = sortedtime[index + 1] - sortedtime[index]
                    self.user_time_feature[user][3] = maxtime
                    self.user_time_feature[user][4] = mintime

            # 活跃天数
            self.user_time_feature[user][5] = min(self.user_days[user])
            self.user_time_feature[user][6] = max(self.user_days[user])
            self.user_time_feature[user][7] = len(self.user_days[user])
            if len(self.user_days[user]) <= 1:
                self.user_time_feature[user][8] = -1
                self.user_time_feature[user][9] = -1
            else:
                sortedtime = sorted(self.user_days[user])
                maxtime = -1
                mintime = 100000
                for index in range(len(sortedtime) - 1):
                    if (sortedtime[index + 1] - sortedtime[index]) > maxtime:
                        maxtime = sortedtime[index + 1] - sortedtime[index]
                    if (sortedtime[index + 1] - sortedtime[index]) < mintime:
                        mintime = sortedtime[index + 1] - sortedtime[index]
                self.user_time_feature[user][8] = maxtime
                self.user_time_feature[user][9] = mintime

            # 最后时间 - 用户第一次活跃时间
            self.user_time_feature[user][10] = enddays - self.user_time_feature[user][5]

            # 购物天数  / 活跃天数
            self.user_time_feature[user][11] = float(self.user_time_feature[user][2]) / self.user_time_feature[user][7]



            if not self.user_buyandclick_feature.has_key(user):
                self.user_buyandclick_feature[user] = [0 ] * 138


            # 用户购买物品次数
            if not self.user_buyitems.has_key(user):
                self.user_buyandclick_feature[user][0] = 0
                self.user_buyandclick_feature[user][1] = 0
                self.user_buyandclick_feature[user][2] = 0
                self.user_buyandclick_feature[user][3] = 0
                self.user_buyandclick_feature[user][4] = 0
                self.user_buyandclick_feature[user][5] = 0
                self.user_buyandclick_feature[user][6] = 0
                self.user_buyandclick_feature[user][7] = 0
                self.user_buyandclick_feature[user][8] = 0
            else:
                countall = 0
                for item in self.user_buyitems[user]['all'].keys():
                    countall = countall + self.user_buyitems[user]['all'][item]

                count_7days = 0
                for item in self.user_buyitems[user]['7'].keys():
                    count_7days = count_7days + self.user_buyitems[user]['7'][item]

                count_15days = 0
                for item in self.user_buyitems[user]['15'].keys():
                    count_15days = count_15days + self.user_buyitems[user]['15'][item]

                count_first1month = 0
                for item in self.user_buyitems[user]['first1month'].keys():
                    count_first1month = count_first1month + self.user_buyitems[user]['first1month'][item]

                count_last1month = 0
                for item in self.user_buyitems[user]['last1month'].keys():
                    count_last1month = count_last1month + self.user_buyitems[user]['last1month'][item]

                count_last2month = 0
                for item in self.user_buyitems[user]['last2month'].keys():
                    count_last2month = count_last2month + self.user_buyitems[user]['last2month'][item]

                self.user_buyandclick_feature[user][0] = countall
                self.user_buyandclick_feature[user][1] = count_7days
                self.user_buyandclick_feature[user][2] = count_15days
                self.user_buyandclick_feature[user][3] = count_last1month
                self.user_buyandclick_feature[user][4] = count_last2month
                self.user_buyandclick_feature[user][5] = count_first1month
                self.user_buyandclick_feature[user][6] = float(countall) / (enddays / 30)
                self.user_buyandclick_feature[user][7] = self.user_buyandclick_feature[user][3] - self.user_buyandclick_feature[user][4]
                self.user_buyandclick_feature[user][8] = self.user_buyandclick_feature[user][3] - self.user_buyandclick_feature[user][5]

            # 购买物品的个数
            if not self.user_buyitems.has_key(user):
                self.user_buyandclick_feature[user][9] = 0
                self.user_buyandclick_feature[user][10] = 0
                self.user_buyandclick_feature[user][11] = 0
                self.user_buyandclick_feature[user][12] = 0
                self.user_buyandclick_feature[user][13] = 0
                self.user_buyandclick_feature[user][14] = 0
                self.user_buyandclick_feature[user][15] = 0
                self.user_buyandclick_feature[user][16] = 0
                self.user_buyandclick_feature[user][17] = 0
            else:
                self.user_buyandclick_feature[user][9] = len(self.user_buyitems[user]['all'].keys())
                self.user_buyandclick_feature[user][10] = len(self.user_buyitems[user]['7'].keys())
                self.user_buyandclick_feature[user][11] = len(self.user_buyitems[user]['15'].keys())
                self.user_buyandclick_feature[user][12] = len(self.user_buyitems[user]['last1month'].keys())
                self.user_buyandclick_feature[user][13] = len(self.user_buyitems[user]['last2month'].keys())
                self.user_buyandclick_feature[user][14] = len(self.user_buyitems[user]['first1month'].keys())
                self.user_buyandclick_feature[user][15] = self.user_buyandclick_feature[user][9] / (enddays / 30)
                self.user_buyandclick_feature[user][16] = self.user_buyandclick_feature[user][12] - self.user_buyandclick_feature[user][13]
                self.user_buyandclick_feature[user][17] = self.user_buyandclick_feature[user][12] - self.user_buyandclick_feature[user][14]


            # 用户点击的物品次数
            if not self.user_clickitems.has_key(user):
                self.user_buyandclick_feature[user][18] = 0
                self.user_buyandclick_feature[user][19] = 0
                self.user_buyandclick_feature[user][20] = 0
                self.user_buyandclick_feature[user][21] = 0
                self.user_buyandclick_feature[user][22] = 0
                self.user_buyandclick_feature[user][23] = 0
                self.user_buyandclick_feature[user][24] = 0
                self.user_buyandclick_feature[user][25] = 0
                self.user_buyandclick_feature[user][26] = 0
            else:
                countall = 0
                for item in self.user_clickitems[user]['all'].keys():
                    countall = countall + self.user_clickitems[user]['all'][item]

                count_7days = 0
                for item in self.user_clickitems[user]['7'].keys():
                    count_7days = count_7days + self.user_clickitems[user]['7'][item]

                count_15days = 0
                for item in self.user_clickitems[user]['15'].keys():
                    count_15days = count_15days + self.user_clickitems[user]['15'][item]

                count_first1month = 0
                for item in self.user_clickitems[user]['first1month'].keys():
                    count_first1month = count_first1month + self.user_clickitems[user]['first1month'][item]

                count_last1month = 0
                for item in self.user_clickitems[user]['last1month'].keys():
                    count_last1month = count_last1month + self.user_clickitems[user]['last1month'][item]

                count_last2month = 0
                for item in self.user_clickitems[user]['last2month'].keys():
                    count_last2month = count_last2month + self.user_clickitems[user]['last2month'][item]

                self.user_buyandclick_feature[user][18] = countall
                self.user_buyandclick_feature[user][19] = count_7days
                self.user_buyandclick_feature[user][20] = count_15days
                self.user_buyandclick_feature[user][21] = count_last1month
                self.user_buyandclick_feature[user][22] = count_last2month
                self.user_buyandclick_feature[user][23] = count_first1month
                self.user_buyandclick_feature[user][24] = float(countall) / (enddays / 30)
                self.user_buyandclick_feature[user][25] = self.user_buyandclick_feature[user][21] - self.user_buyandclick_feature[user][22]
                self.user_buyandclick_feature[user][26] = self.user_buyandclick_feature[user][21] - self.user_buyandclick_feature[user][23]

            # 点击物品的个数
            if not self.user_clickitems.has_key(user):
                self.user_buyandclick_feature[user][27] = 0
                self.user_buyandclick_feature[user][28] = 0
                self.user_buyandclick_feature[user][29] = 0
                self.user_buyandclick_feature[user][30] = 0
                self.user_buyandclick_feature[user][31] = 0
                self.user_buyandclick_feature[user][32] = 0
                self.user_buyandclick_feature[user][33] = 0
                self.user_buyandclick_feature[user][34] = 0
                self.user_buyandclick_feature[user][35] = 0
            else:
                self.user_buyandclick_feature[user][27] = len(self.user_clickitems[user]['all'].keys())
                self.user_buyandclick_feature[user][28] = len(self.user_clickitems[user]['7'].keys())
                self.user_buyandclick_feature[user][29] = len(self.user_clickitems[user]['15'].keys())
                self.user_buyandclick_feature[user][30] = len(self.user_clickitems[user]['last1month'].keys())
                self.user_buyandclick_feature[user][31] = len(self.user_clickitems[user]['last2month'].keys())
                self.user_buyandclick_feature[user][32] = len(self.user_clickitems[user]['first1month'].keys())
                self.user_buyandclick_feature[user][33] = self.user_buyandclick_feature[user][27] / (enddays / 30)
                self.user_buyandclick_feature[user][34] = self.user_buyandclick_feature[user][30] - self.user_buyandclick_feature[user][31]
                self.user_buyandclick_feature[user][35] = self.user_buyandclick_feature[user][30] - self.user_buyandclick_feature[user][32]


            # 用户购买的的类别个数
            if not self.user_buycategory.has_key(user):
                self.user_buyandclick_feature[user][36] = 0
                self.user_buyandclick_feature[user][37] = 0
                self.user_buyandclick_feature[user][38] = 0
                self.user_buyandclick_feature[user][39] = 0
                self.user_buyandclick_feature[user][40] = 0
                self.user_buyandclick_feature[user][41] = 0
                self.user_buyandclick_feature[user][42] = 0
                self.user_buyandclick_feature[user][43] = 0
                self.user_buyandclick_feature[user][44] = 0
            else:
                self.user_buyandclick_feature[user][36] = len(self.user_buycategory[user]['all'].keys())
                self.user_buyandclick_feature[user][37] = len(self.user_buycategory[user]['7'].keys())
                self.user_buyandclick_feature[user][38] = len(self.user_buycategory[user]['15'].keys())
                self.user_buyandclick_feature[user][39] = len(self.user_buycategory[user]['last1month'].keys())
                self.user_buyandclick_feature[user][40] = len(self.user_buycategory[user]['last2month'].keys())
                self.user_buyandclick_feature[user][41] = len(self.user_buycategory[user]['first1month'].keys())
                self.user_buyandclick_feature[user][42] = self.user_buyandclick_feature[user][36] / (enddays / 30)
                self.user_buyandclick_feature[user][43] = self.user_buyandclick_feature[user][39] - self.user_buyandclick_feature[user][40]
                self.user_buyandclick_feature[user][44] = self.user_buyandclick_feature[user][39] - self.user_buyandclick_feature[user][41]


            # 用户点击的类别的个数
            if not self.user_clickcategory.has_key(user):
                self.user_buyandclick_feature[user][45] = 0
                self.user_buyandclick_feature[user][46] = 0
                self.user_buyandclick_feature[user][47] = 0
                self.user_buyandclick_feature[user][48] = 0
                self.user_buyandclick_feature[user][49] = 0
                self.user_buyandclick_feature[user][50] = 0
                self.user_buyandclick_feature[user][51] = 0
                self.user_buyandclick_feature[user][52] = 0
                self.user_buyandclick_feature[user][53] = 0
            else:
                self.user_buyandclick_feature[user][45] = len(self.user_clickcategory[user]['all'].keys())
                self.user_buyandclick_feature[user][46] = len(self.user_clickcategory[user]['7'].keys())
                self.user_buyandclick_feature[user][47] = len(self.user_clickcategory[user]['15'].keys())
                self.user_buyandclick_feature[user][48] = len(self.user_clickcategory[user]['last1month'].keys())
                self.user_buyandclick_feature[user][49] = len(self.user_clickcategory[user]['last2month'].keys())
                self.user_buyandclick_feature[user][50] = len(self.user_clickcategory[user]['first1month'].keys())
                self.user_buyandclick_feature[user][51] = self.user_buyandclick_feature[user][45] / (enddays / 30)
                self.user_buyandclick_feature[user][52] = self.user_buyandclick_feature[user][48] - self.user_buyandclick_feature[user][49]
                self.user_buyandclick_feature[user][53] = self.user_buyandclick_feature[user][48] - self.user_buyandclick_feature[user][50]

            # 用户购买商家的个数
            if not self.user_buyseller.has_key(user):
                self.user_buyandclick_feature[user][54] = 0
                self.user_buyandclick_feature[user][55] = 0
                self.user_buyandclick_feature[user][56] = 0
                self.user_buyandclick_feature[user][57] = 0
                self.user_buyandclick_feature[user][58] = 0
                self.user_buyandclick_feature[user][59] = 0
                self.user_buyandclick_feature[user][60] = 0
                self.user_buyandclick_feature[user][61] = 0
                self.user_buyandclick_feature[user][62] = 0
            else:
                self.user_buyandclick_feature[user][54] = len(self.user_buyseller[user]['all'].keys())
                self.user_buyandclick_feature[user][55] = len(self.user_buyseller[user]['7'].keys())
                self.user_buyandclick_feature[user][56] = len(self.user_buyseller[user]['15'].keys())
                self.user_buyandclick_feature[user][57] = len(self.user_buyseller[user]['last1month'].keys())
                self.user_buyandclick_feature[user][58] = len(self.user_buyseller[user]['last2month'].keys())
                self.user_buyandclick_feature[user][59] = len(self.user_buyseller[user]['first1month'].keys())
                self.user_buyandclick_feature[user][60] = self.user_buyandclick_feature[user][54] / (enddays / 30)
                self.user_buyandclick_feature[user][61] = self.user_buyandclick_feature[user][57] - self.user_buyandclick_feature[user][58]
                self.user_buyandclick_feature[user][62] = self.user_buyandclick_feature[user][57] - self.user_buyandclick_feature[user][59]


            # 用户点击商家的个数
            if not self.user_clickseller.has_key(user):
                self.user_buyandclick_feature[user][63] = 0
                self.user_buyandclick_feature[user][64] = 0
                self.user_buyandclick_feature[user][65] = 0
                self.user_buyandclick_feature[user][66] = 0
                self.user_buyandclick_feature[user][67] = 0
                self.user_buyandclick_feature[user][68] = 0
                self.user_buyandclick_feature[user][69] = 0
                self.user_buyandclick_feature[user][70] = 0
                self.user_buyandclick_feature[user][71] = 0
            else:
                self.user_buyandclick_feature[user][63] = len(self.user_clickseller[user]['all'].keys())
                self.user_buyandclick_feature[user][64] = len(self.user_clickseller[user]['7'].keys())
                self.user_buyandclick_feature[user][65] = len(self.user_clickseller[user]['15'].keys())
                self.user_buyandclick_feature[user][66] = len(self.user_clickseller[user]['last1month'].keys())
                self.user_buyandclick_feature[user][67] = len(self.user_clickseller[user]['last2month'].keys())
                self.user_buyandclick_feature[user][68] = len(self.user_clickseller[user]['first1month'].keys())
                self.user_buyandclick_feature[user][69] = self.user_buyandclick_feature[user][63] / (enddays / 30)
                self.user_buyandclick_feature[user][70] = self.user_buyandclick_feature[user][66] - self.user_buyandclick_feature[user][67]
                self.user_buyandclick_feature[user][71] = self.user_buyandclick_feature[user][66] - self.user_buyandclick_feature[user][68]


            #  用户购买物品的次数   / 用户点击物品的次数
            if self.user_buyandclick_feature[user][18] == 0 :
                self.user_buyandclick_feature[user][72] = 0
            else:
                self.user_buyandclick_feature[user][72] = float(self.user_buyandclick_feature[user][0]) / self.user_buyandclick_feature[user][18]

            if self.user_buyandclick_feature[user][19] == 0:
                self.user_buyandclick_feature[user][73] = 0
            else:
                self.user_buyandclick_feature[user][73] = float(self.user_buyandclick_feature[user][1]) / self.user_buyandclick_feature[user][19]

            if self.user_buyandclick_feature[user][20] == 0:
                self.user_buyandclick_feature[user][74] = 0
            else:
                self.user_buyandclick_feature[user][74] = float(self.user_buyandclick_feature[user][2]) / self.user_buyandclick_feature[user][20]

            if self.user_buyandclick_feature[user][21] == 0:
                self.user_buyandclick_feature[user][75] = 0
            else:
                self.user_buyandclick_feature[user][75] = float(self.user_buyandclick_feature[user][3]) / self.user_buyandclick_feature[user][21]

            if self.user_buyandclick_feature[user][22] == 0:
                self.user_buyandclick_feature[user][76] = 0
            else:
                self.user_buyandclick_feature[user][76] = float(self.user_buyandclick_feature[user][4]) / self.user_buyandclick_feature[user][22]

            if self.user_buyandclick_feature[user][23] == 0:
                self.user_buyandclick_feature[user][77] = 0
            else:
                self.user_buyandclick_feature[user][77] = float(self.user_buyandclick_feature[user][5]) / self.user_buyandclick_feature[user][23]

            # 用户购买类别的次数  / 用户点击类别的次数
            if self.user_buyandclick_feature[user][45] == 0:
                self.user_buyandclick_feature[user][78] = 0
            else:
                self.user_buyandclick_feature[user][78] = float(self.user_buyandclick_feature[user][36]) / self.user_buyandclick_feature[user][45]

            if self.user_buyandclick_feature[user][46] == 0:
                self.user_buyandclick_feature[user][79] = 0
            else:
                self.user_buyandclick_feature[user][79] = float(self.user_buyandclick_feature[user][37]) / self.user_buyandclick_feature[user][46]

            if self.user_buyandclick_feature[user][47] == 0:
                self.user_buyandclick_feature[user][80] = 0
            else:
                self.user_buyandclick_feature[user][80] = float(self.user_buyandclick_feature[user][38]) / self.user_buyandclick_feature[user][47]

            if self.user_buyandclick_feature[user][48] == 0:
                self.user_buyandclick_feature[user][81] = 0
            else:
                self.user_buyandclick_feature[user][81] = float(self.user_buyandclick_feature[user][39]) / self.user_buyandclick_feature[user][48]

            if self.user_buyandclick_feature[user][49] == 0:
                self.user_buyandclick_feature[user][82] = 0
            else:
                self.user_buyandclick_feature[user][82] = float(self.user_buyandclick_feature[user][40]) / self.user_buyandclick_feature[user][49]

            if self.user_buyandclick_feature[user][50] == 0:
                self.user_buyandclick_feature[user][83] = 0
            else:
                self.user_buyandclick_feature[user][83] = float(self.user_buyandclick_feature[user][41]) / self.user_buyandclick_feature[user][50]

            # 用户购买商家的次数 / 用户点击商家的次数
            if self.user_buyandclick_feature[user][63] == 0:
                self.user_buyandclick_feature[user][84] = 0
            else:
                self.user_buyandclick_feature[user][84] = float(self.user_buyandclick_feature[user][54]) / self.user_buyandclick_feature[user][63]

            if self.user_buyandclick_feature[user][64] == 0:
                self.user_buyandclick_feature[user][85] = 0
            else:
                self.user_buyandclick_feature[user][85] = float(self.user_buyandclick_feature[user][55]) / self.user_buyandclick_feature[user][64]

            if self.user_buyandclick_feature[user][65] == 0:
                self.user_buyandclick_feature[user][86] = 0
            else:
                self.user_buyandclick_feature[user][86] = float(self.user_buyandclick_feature[user][56]) / self.user_buyandclick_feature[user][65]

            if self.user_buyandclick_feature[user][66] == 0:
                self.user_buyandclick_feature[user][87] = 0
            else:
                self.user_buyandclick_feature[user][87] = float(self.user_buyandclick_feature[user][57]) / self.user_buyandclick_feature[user][66]

            if self.user_buyandclick_feature[user][67] == 0:
                self.user_buyandclick_feature[user][88] = 0
            else:
                self.user_buyandclick_feature[user][88] = float(self.user_buyandclick_feature[user][58]) / self.user_buyandclick_feature[user][67]

            if self.user_buyandclick_feature[user][68] == 0:
                self.user_buyandclick_feature[user][89] = 0
            else:
                self.user_buyandclick_feature[user][89] = float(self.user_buyandclick_feature[user][59]) / self.user_buyandclick_feature[user][68]


            # 用户购买1次商品数，用户购买2次商品数，用户购买3次商品数，购买次数商品数 / 用户购买商品数
            if not self.user_buyitems.has_key(user):
                self.user_buyandclick_feature[user][90] = 0
                self.user_buyandclick_feature[user][91] = 0
                self.user_buyandclick_feature[user][92] = 0
                self.user_buyandclick_feature[user][93] = 0
                self.user_buyandclick_feature[user][94] = 0
                self.user_buyandclick_feature[user][95] = 0
                self.user_buyandclick_feature[user][96] = 0
                self.user_buyandclick_feature[user][97] = 0
            else:
                count_1 = 0
                count_2 = 0
                count_3 = 0
                count_3plus = 0
                allcount = len(self.user_buyitems[user]['all'].keys())
                for item in self.user_buyitems[user]['all'].keys():
                    if self.user_buyitems[user]['all'][item] == 1:
                        count_1 += 1
                    if self.user_buyitems[user]['all'][item] == 2:
                        count_2 += 1
                    if self.user_buyitems[user]['all'][item] == 3:
                        count_3 += 1
                    if self.user_buyitems[user]['all'][item] > 3:
                        count_3plus += 1
                self.user_buyandclick_feature[user][90] = count_1
                self.user_buyandclick_feature[user][91] = count_2
                self.user_buyandclick_feature[user][92] = count_3
                self.user_buyandclick_feature[user][93] = count_3plus
                self.user_buyandclick_feature[user][94] = float(count_1) / allcount
                self.user_buyandclick_feature[user][95] = float(count_2) / allcount
                self.user_buyandclick_feature[user][96] = float(count_3) / allcount
                self.user_buyandclick_feature[user][97] = float(count_3plus) / allcount

            # 用户点击1次商品数，点击2次商品数，点击3次商品数，点击次数商品 / 总的点击商品数
            if not self.user_clickitems.has_key(user):
                self.user_buyandclick_feature[user][98] = 0
                self.user_buyandclick_feature[user][99] = 0
                self.user_buyandclick_feature[user][100] = 0
                self.user_buyandclick_feature[user][101] = 0
                self.user_buyandclick_feature[user][102] = 0
                self.user_buyandclick_feature[user][103] = 0
                self.user_buyandclick_feature[user][104] = 0
                self.user_buyandclick_feature[user][105] = 0
            else:
                count_1 = 0
                count_2 = 0
                count_3 = 0
                count_3plus = 0
                allcount = len(self.user_clickitems[user]['all'].keys())
                for item in self.user_clickitems[user]['all'].keys():
                    if self.user_clickitems[user]['all'][item] == 1:
                        count_1 += 1
                    if self.user_clickitems[user]['all'][item] == 2:
                        count_2 += 1
                    if self.user_clickitems[user]['all'][item] == 3:
                        count_3 += 1
                    if self.user_clickitems[user]['all'][item] > 3:
                        count_3plus += 1
                self.user_buyandclick_feature[user][98] = count_1
                self.user_buyandclick_feature[user][99] = count_2
                self.user_buyandclick_feature[user][100] = count_3
                self.user_buyandclick_feature[user][101] = count_3plus
                self.user_buyandclick_feature[user][102] = float(count_1) / allcount
                self.user_buyandclick_feature[user][103] = float(count_2) / allcount
                self.user_buyandclick_feature[user][104] = float(count_3) / allcount
                self.user_buyandclick_feature[user][105] = float(count_3plus) / allcount

            # 用户购买的1次类别数， 类别次数/类别数
            if not self.user_buycategory.has_key(user):
                self.user_buyandclick_feature[user][106] = 0
                self.user_buyandclick_feature[user][107] = 0
                self.user_buyandclick_feature[user][108] = 0
                self.user_buyandclick_feature[user][109] = 0
                self.user_buyandclick_feature[user][110] = 0
                self.user_buyandclick_feature[user][111] = 0
                self.user_buyandclick_feature[user][112] = 0
                self.user_buyandclick_feature[user][113] = 0
            else:
                count_1 = 0
                count_2 = 0
                count_3 = 0
                count_3plus = 0
                allcount = len(self.user_buycategory[user]['all'].keys())
                for cate in self.user_buycategory[user]['all'].keys():
                    if self.user_buycategory[user]['all'][cate] == 1:
                        count_1 += 1
                    if self.user_buycategory[user]['all'][cate] == 2:
                        count_2 += 1
                    if self.user_buycategory[user]['all'][cate] == 3:
                        count_3 += 1
                    if self.user_buycategory[user]['all'][cate] > 3:
                        count_3plus += 1
                self.user_buyandclick_feature[user][106] = count_1
                self.user_buyandclick_feature[user][107] = count_2
                self.user_buyandclick_feature[user][108] = count_3
                self.user_buyandclick_feature[user][109] = count_3plus
                self.user_buyandclick_feature[user][110] = float(count_1) / allcount
                self.user_buyandclick_feature[user][111] = float(count_2) / allcount
                self.user_buyandclick_feature[user][112] = float(count_3) / allcount
                self.user_buyandclick_feature[user][113] = float(count_3plus) / allcount

            # 用户点击的类别数，类别次数 / 类别数
            if not self.user_clickcategory.has_key(user):
                self.user_buyandclick_feature[user][114] = 0
                self.user_buyandclick_feature[user][115] = 0
                self.user_buyandclick_feature[user][116] = 0
                self.user_buyandclick_feature[user][117] = 0
                self.user_buyandclick_feature[user][118] = 0
                self.user_buyandclick_feature[user][119] = 0
                self.user_buyandclick_feature[user][120] = 0
                self.user_buyandclick_feature[user][121] = 0
            else:
                count_1 = 0
                count_2 = 0
                count_3 = 0
                count_3plus = 0
                allcount = len(self.user_clickcategory[user]['all'].keys())
                for cate in self.user_clickcategory[user]['all'].keys():
                    if self.user_clickcategory[user]['all'][cate] == 1:
                        count_1 += 1
                    if self.user_clickcategory[user]['all'][cate] == 2:
                        count_2 += 1
                    if self.user_clickcategory[user]['all'][cate] == 3:
                        count_3 += 1
                    if self.user_clickcategory[user]['all'][cate] > 3:
                        count_3plus += 1
                self.user_buyandclick_feature[user][114] = count_1
                self.user_buyandclick_feature[user][115] = count_2
                self.user_buyandclick_feature[user][116] = count_3
                self.user_buyandclick_feature[user][117] = count_3plus
                self.user_buyandclick_feature[user][118] = float(count_1) / allcount
                self.user_buyandclick_feature[user][119] = float(count_2) / allcount
                self.user_buyandclick_feature[user][120] = float(count_3) / allcount
                self.user_buyandclick_feature[user][121] = float(count_3plus) / allcount

            # 用户购买商家次数， 用户购买商家次数 / 购买的商家的数
            if not self.user_buyseller.has_key(user):
                self.user_buyandclick_feature[user][122] = 0
                self.user_buyandclick_feature[user][123] = 0
                self.user_buyandclick_feature[user][124] = 0
                self.user_buyandclick_feature[user][125] = 0
                self.user_buyandclick_feature[user][126] = 0
                self.user_buyandclick_feature[user][127] = 0
                self.user_buyandclick_feature[user][128] = 0
                self.user_buyandclick_feature[user][129] = 0
            else:
                count_1 = 0
                count_2 = 0
                count_3 = 0
                count_3plus = 0
                allcount = len(self.user_buyseller[user]['all'].keys())
                for sell in self.user_buyseller[user]['all'].keys():
                    if self.user_buyseller[user]['all'][sell] == 1:
                        count_1 += 1
                    if self.user_buyseller[user]['all'][sell] == 2:
                        count_2 += 1
                    if self.user_buyseller[user]['all'][sell] == 3:
                        count_3 += 1
                    if self.user_buyseller[user]['all'][sell] > 3:
                        count_3plus += 1
                self.user_buyandclick_feature[user][122] = count_1
                self.user_buyandclick_feature[user][123] = count_2
                self.user_buyandclick_feature[user][124] = count_3
                self.user_buyandclick_feature[user][125] = count_3plus
                self.user_buyandclick_feature[user][126] = float(count_1) / allcount
                self.user_buyandclick_feature[user][127] = float(count_2) / allcount
                self.user_buyandclick_feature[user][128] = float(count_3) / allcount
                self.user_buyandclick_feature[user][129] = float(count_3plus) / allcount

            # 用户点击的商家次数， 用户点击的商家次数 / 用户点击的商家数
            if not self.user_clickseller.has_key(user):
                self.user_buyandclick_feature[user][130] = 0
                self.user_buyandclick_feature[user][131] = 0
                self.user_buyandclick_feature[user][132] = 0
                self.user_buyandclick_feature[user][133] = 0
                self.user_buyandclick_feature[user][134] = 0
                self.user_buyandclick_feature[user][135] = 0
                self.user_buyandclick_feature[user][136] = 0
                self.user_buyandclick_feature[user][137] = 0
            else:
                count_1 = 0
                count_2 = 0
                count_3 = 0
                count_3plus = 0
                allcount = len(self.user_clickseller[user]['all'].keys())
                for sell in self.user_clickseller[user]['all'].keys():
                    if self.user_clickseller[user]['all'][sell] == 1:
                        count_1 += 1
                    if self.user_clickseller[user]['all'][sell] == 2:
                        count_2 += 1
                    if self.user_clickseller[user]['all'][sell] == 3:
                        count_3 += 1
                    if self.user_clickseller[user]['all'][sell] > 3:
                        count_3plus += 1
                self.user_buyandclick_feature[user][130] = count_1
                self.user_buyandclick_feature[user][131] = count_2
                self.user_buyandclick_feature[user][132] = count_3
                self.user_buyandclick_feature[user][133] = count_3plus
                self.user_buyandclick_feature[user][134] = float(count_1) / allcount
                self.user_buyandclick_feature[user][135] = float(count_2) / allcount
                self.user_buyandclick_feature[user][136] = float(count_3) / allcount
                self.user_buyandclick_feature[user][137] = float(count_3plus) / allcount



    def mergeTaobaoUserFeature(self, enddays):


        self.getTaobaoUserBasevalue(enddays)
        self.getTaobaoDivvalue(enddays)
        print 'merget the taobao user feature ...'

        for user in self.user_time_feature.keys():
            if not self.taobao_userFeature.has_key(user):
                self.taobao_userFeature[user] = []
            self.taobao_userFeature[user].extend(self.user_time_feature[user])
            self.taobao_userFeature[user].extend(self.user_buyandclick_feature[user])


if __name__ == '__main__':

    tb = taobaoUserFeature()
    tb.mergeTaobaoUserFeature(153)
    for user in tb.taobao_userFeature.keys():
        print user, '   ', tb.taobao_userFeature[user]
