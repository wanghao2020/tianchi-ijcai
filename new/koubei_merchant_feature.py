# coding=utf-8

# 抽取口碑商家特征

class koubeiMerchantFeature():


    # time (merchant, location)

    # location

    # merchant

    # dummy code
    merchantid_dummycode = {}

    merchant_time = {}
    merchant_locations = {}
    location_merchants = {}
    merchant_person_times = {}
    location_person_times = {}

    merchant_time_feature = {}
    merchant_person_feature = {}

    koubei_merchant_feature = {}

    # merchant_id_dummy_code {merchant:str(code)}
    def getMerchantid_dummycode(self):
        file = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_merchant_info'
        print 'Get the merchant dummy code ...'
        with open(file) as f:
            for line in f:
                line = line.strip('\r\n')
                merchant, budget, locationlist = line.split(',')
                if not self.merchantid_dummycode.has_key(merchant):
                    temp = bin(int(merchant)).replace('0b', '')
                    zeros = ''
                    for i in range(14 - len(temp)):
                        zeros += '0'
                    temp = zeros + temp
                    self.merchantid_dummycode[merchant] = [0] * 14
                    for i in range(14):
                        self.merchantid_dummycode[merchant][i] = int(temp[i])


    def getMerchantAndLocation(self):

        file = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_merchant_info'
        with open(file, 'rb') as f :
            for line in f :
                line = line.strip('\r\n')
                merchant, budget, locationlist = line.split(',')
                locations = locationlist.split(':')
                for location in locations:
                    # merchant :  location
                    if not self.merchant_locations.has_key(merchant):
                        self.merchant_locations[merchant] = []
                    if location not in self.merchant_locations[merchant]:
                        self.merchant_locations[merchant].append(location)

                    # location : merchant
                    if not self.location_merchants.has_key(location):
                        self.location_merchants[location] = []
                    if merchant not in self.location_merchants[location]:
                        self.location_merchants[location].append(merchant)

    def getMerchantBasevalue(self, enddays):

        if enddays == 123:
            endmonth = 10
        if enddays == 153:
            endmonth = 11

        print 'Get the merchant base value ...'
        file = '/home/wanghao/Document/tianchi/dataset/dataset_t/trainfrom7to%d_t' % (endmonth)
        with open(file, 'rb') as f :
            for line in f:
                line = line.strip('\r\n')
                user, merchant, location, time = line.split(',')
                time = int(time)

                # -------- time --------
                if not self.merchant_time.has_key((merchant,location)):
                    self.merchant_time[(merchant,location)] = []
                if time not in self.merchant_time[(merchant,location)]:
                    self.merchant_time[(merchant,location)].append(time)

                # --------- merchant : person  : time
                if not self.merchant_person_times.has_key((merchant,location)):
                    self.merchant_person_times[(merchant,location)] = {}
                    self.merchant_person_times[(merchant,location)]['all'] = {}
                    self.merchant_person_times[(merchant,location)]['7'] = {}
                    self.merchant_person_times[(merchant,location)]['15'] = {}
                    self.merchant_person_times[(merchant,location)]['first1month'] = {}
                    self.merchant_person_times[(merchant,location)]['last1month'] = {}
                    self.merchant_person_times[(merchant,location)]['last2month'] = {}

                if user not in self.merchant_person_times[(merchant,location)]['all']:
                    self.merchant_person_times[(merchant,location)]['all'][user] = 0
                self.merchant_person_times[(merchant, location)]['all'][user] += 1


                if time <= 31:
                    if user not in self.merchant_person_times[(merchant,location)]['first1month']:
                        self.merchant_person_times[(merchant,location)]['first1month'][user] = 0
                    self.merchant_person_times[(merchant, location)]['first1month'][user] += 1

                if (time >= enddays - 31) and time < enddays:
                    if user not in self.merchant_person_times[(merchant, location)]['last1month']:
                        self.merchant_person_times[(merchant, location)]['last1month'][user] = 0
                    self.merchant_person_times[(merchant, location)]['last1month'][user] += 1

                if (time >= enddays - 62) and time < enddays - 31:
                    if user not in self.merchant_person_times[(merchant, location)]['last2month']:
                        self.merchant_person_times[(merchant, location)]['last2month'][user] = 0
                    self.merchant_person_times[(merchant, location)]['last2month'][user] += 1

                if (time >= enddays - 7) and time < enddays:
                    if user not in self.merchant_person_times[(merchant, location)]['7']:
                        self.merchant_person_times[(merchant, location)]['7'][user] = 0
                    self.merchant_person_times[(merchant, location)]['7'][user] += 1

                if (time >= enddays - 15) and time < enddays:
                    if user not in self.merchant_person_times[(merchant, location)]['15']:
                        self.merchant_person_times[(merchant, location)]['15'][user] = 0
                    self.merchant_person_times[(merchant, location)]['15'][user] += 1

                # ---------- location  : person  :  time
                if not self.location_person_times.has_key(location):
                    self.location_person_times[location] = {}
                    self.location_person_times[location]['all'] = {}
                    self.location_person_times[location]['7'] = {}
                    self.location_person_times[location]['15'] = {}
                    self.location_person_times[location]['first1month'] = {}
                    self.location_person_times[location]['last1month'] = {}
                    self.location_person_times[location]['last2month'] = {}

                if not self.location_person_times[location]['all'].has_key(user):
                    self.location_person_times[location]['all'][user] = 0
                self.location_person_times[location]['all'][user] += 1

                if time <= 31:
                    if not self.location_person_times[location]['first1month'].has_key(user):
                        self.location_person_times[location]['first1month'][user] = 0
                    self.location_person_times[ location]['first1month'][user] += 1

                if (time >= enddays - 31) and time < enddays:
                    if not self.location_person_times[location]['last1month'].has_key(user):
                        self.location_person_times[location]['last1month'][user] = 0
                    self.location_person_times[location]['last1month'][user] += 1

                if (time >= enddays - 62) and time < enddays - 31:
                    if not self.location_person_times[location]['last2month'].has_key(user):
                        self.location_person_times[location]['last2month'][user] = 0
                    self.location_person_times[location]['last2month'][user] += 1

                if (time >= enddays - 7) and time < enddays:
                    if not self.location_person_times[location]['7'].has_key(user):
                        self.location_person_times[location]['7'][user] = 0
                    self.location_person_times[location]['7'][user] += 1

                if (time >= enddays - 15) and time < enddays:
                    if not self.location_person_times[location]['15'].has_key(user):
                        self.location_person_times[location]['15'][user] = 0
                    self.location_person_times[location]['15'][user] += 1

    def getMerchantDivvalue(self, enddays):
        print 'Get the merchant div value ...'

        # ----- merchant time feature-------
        for key in self.merchant_time.keys():
            if not self.merchant_time_feature.has_key(key):
                self.merchant_time_feature[key] = [0] * 8

            sortedtime = sorted(self.merchant_time[key])
            self.merchant_time_feature[key][0] = min(sortedtime)
            self.merchant_time_feature[key][1] = max(sortedtime)
            self.merchant_time_feature[key][2] = enddays - min(sortedtime)
            self.merchant_time_feature[key][3] = len(sortedtime)

            if len(sortedtime) <= 1:
                self.merchant_time_feature[key][4] = -1
                self.merchant_time_feature[key][5] = -1
                self.merchant_time_feature[key][6] = -1
            else:
                maxtime = -1
                mintime = 100000
                alltime = 0
                for index in range(len(sortedtime) - 1):
                    if (sortedtime[index + 1] - sortedtime[index]) > maxtime:
                        maxtime = sortedtime[index + 1] - sortedtime[index]
                    if (sortedtime[index + 1] - sortedtime[index]) < mintime:
                        mintime = sortedtime[index + 1] - sortedtime[index]
                    alltime = alltime + sortedtime[index + 1] - sortedtime[index]

                self.merchant_time_feature[key][4] = maxtime
                self.merchant_time_feature[key][5] = mintime
                self.merchant_time_feature[key][6] = float(alltime) / (len(sortedtime) - 1)

            self.merchant_time_feature[key][7] = float(self.merchant_time_feature[key][1] - self.merchant_time_feature[key][0]) / self.merchant_time_feature[key][3]


        # ------merchant person feature
        for key in self.merchant_person_times.keys():
            if not self.merchant_person_feature.has_key(key):
                self.merchant_person_feature[key] = [0] * 56

            #-------> 商家的人次数
            count_all = 0
            for person in self.merchant_person_times[key]['all'].keys():
                count_all = count_all + self.merchant_person_times[key]['all'][person]
            self.merchant_person_feature[key][0] = count_all

            count_7days = 0
            for person in self.merchant_person_times[key]['7'].keys():
                count_7days = count_7days + self.merchant_person_times[key]['7'][person]
            self.merchant_person_feature[key][1] = count_7days

            count_15days = 0
            for person in self.merchant_person_times[key]['15'].keys():
                count_15days = count_15days + self.merchant_person_times[key]['15'][person]
            self.merchant_person_feature[key][2] = count_15days

            count_first1month = 0
            for person in self.merchant_person_times[key]['first1month'].keys():
                count_first1month = count_first1month + self.merchant_person_times[key]['first1month'][person]
            self.merchant_person_feature[key][3] = count_first1month

            count_last1month = 0
            for person in self.merchant_person_times[key]['last1month'].keys():
                count_last1month = count_last1month + self.merchant_person_times[key]['last1month'][person]
            self.merchant_person_feature[key][4] = count_last1month

            count_last2month = 0
            for person in self.merchant_person_times[key]['last2month'].keys():
                count_last2month = count_last2month + self.merchant_person_times[key]['last2month'][person]
            self.merchant_person_feature[key][5] = count_last2month

            # increase
            self.merchant_person_feature[key][6] = self.merchant_person_feature[key][4] - self.merchant_person_feature[key][5]
            self.merchant_person_feature[key][7] = self.merchant_person_feature[key][4] - self.merchant_person_feature[key][3]

            # avg
            self.merchant_person_feature[key][8] = float(self.merchant_person_feature[key][0]) / (enddays/30)


            #-------> 商家的用户数
            self.merchant_person_feature[key][9] = len(self.merchant_person_times[key]['all'].keys())
            self.merchant_person_feature[key][10] = len(self.merchant_person_times[key]['7'].keys())
            self.merchant_person_feature[key][11] = len(self.merchant_person_times[key]['15'].keys())
            self.merchant_person_feature[key][12] = len(self.merchant_person_times[key]['first1month'].keys())
            self.merchant_person_feature[key][13] = len(self.merchant_person_times[key]['last1month'].keys())
            self.merchant_person_feature[key][14] = len(self.merchant_person_times[key]['last2month'].keys())

            # increase
            self.merchant_person_feature[key][15] = self.merchant_person_feature[key][13] - self.merchant_person_feature[key][14]
            self.merchant_person_feature[key][16] = self.merchant_person_feature[key][13] - self.merchant_person_feature[key][12]

            # avg
            self.merchant_person_feature[key][17] = float(self.merchant_person_feature[key][9]) / (enddays/30)

            #---------- 该地点下的总人次数
            count_all = 0
            for person in self.location_person_times[key[1]]['all'].keys():
                count_all = count_all + self.location_person_times[key[1]]['all'][person]
            self.merchant_person_feature[key][18] = count_all

            count_7days = 0
            for person in self.location_person_times[key[1]]['7'].keys():
                count_7days = count_7days + self.location_person_times[key[1]]['7'][person]
            self.merchant_person_feature[key][19] = count_7days

            count_15days = 0
            for person in self.location_person_times[key[1]]['15'].keys():
                count_15days = count_15days + self.location_person_times[key[1]]['15'][person]
            self.merchant_person_feature[key][20] = count_15days

            count_first1month = 0
            for person in self.location_person_times[key[1]]['first1month'].keys():
                count_first1month = count_first1month + self.location_person_times[key[1]]['first1month'][person]
            self.merchant_person_feature[key][21] = count_first1month

            count_last1month = 0
            for person in self.location_person_times[key[1]]['last1month'].keys():
                count_last1month = count_last1month + self.location_person_times[key[1]]['last1month'][person]
            self.merchant_person_feature[key][22] = count_last1month

            count_last2month = 0
            for person in self.location_person_times[key[1]]['last2month'].keys():
                count_last2month = count_last2month + self.location_person_times[key[1]]['last2month'][person]
            self.merchant_person_feature[key][23] = count_last2month

            # increase
            self.merchant_person_feature[key][24] = self.merchant_person_feature[key][22] - self.merchant_person_feature[key][23]
            self.merchant_person_feature[key][25] = self.merchant_person_feature[key][22] - self.merchant_person_feature[key][21]

            # avg
            self.merchant_person_feature[key][26] = float(self.merchant_person_feature[key][18]) / (enddays / 30)

            # -------- 该地点下总用户数
            self.merchant_person_feature[key][27] = len(self.location_person_times[key[1]]['all'].keys())
            self.merchant_person_feature[key][28] = len(self.location_person_times[key[1]]['7'].keys())
            self.merchant_person_feature[key][29] = len(self.location_person_times[key[1]]['15'].keys())
            self.merchant_person_feature[key][30] = len(self.location_person_times[key[1]]['first1month'].keys())
            self.merchant_person_feature[key][31] = len(self.location_person_times[key[1]]['last1month'].keys())
            self.merchant_person_feature[key][32] = len(self.location_person_times[key[1]]['last2month'].keys())

            # increase
            self.merchant_person_feature[key][33] = self.merchant_person_feature[key][31] - self.merchant_person_feature[key][32]
            self.merchant_person_feature[key][34] = self.merchant_person_feature[key][31] - self.merchant_person_feature[key][30]

            # avg
            self.merchant_person_feature[key][35] = float(self.merchant_person_feature[key][27]) / (enddays / 30)

            # 该商家人次数 / 该地点下的人次数
            if self.merchant_person_feature[key][18] == 0:
                self.merchant_person_feature[key][36] = 0
            else:
                self.merchant_person_feature[key][36] = float(self.merchant_person_feature[key][0]) / self.merchant_person_feature[key][18]

            if self.merchant_person_feature[key][19] == 0:
                self.merchant_person_feature[key][37] = 0
            else:
                self.merchant_person_feature[key][37] = float(self.merchant_person_feature[key][1]) / self.merchant_person_feature[key][19]

            if self.merchant_person_feature[key][20] == 0:
                self.merchant_person_feature[key][38] = 0
            else:
                self.merchant_person_feature[key][38] = float(self.merchant_person_feature[key][2]) / self.merchant_person_feature[key][20]

            if self.merchant_person_feature[key][21] == 0:
                self.merchant_person_feature[key][39] = 0
            else:
                self.merchant_person_feature[key][39] = float(self.merchant_person_feature[key][3]) / self.merchant_person_feature[key][21]

            if self.merchant_person_feature[key][22] == 0:
                self.merchant_person_feature[key][40] = 0
            else:
                self.merchant_person_feature[key][40] = float(self.merchant_person_feature[key][4]) / self.merchant_person_feature[key][22]

            if self.merchant_person_feature[key][23] == 0:
                self.merchant_person_feature[key][41] = 0
            else:
                self.merchant_person_feature[key][41] = float(self.merchant_person_feature[key][5]) / self.merchant_person_feature[key][23]


            # 该商家用户数 / 该地点下的用户数
            if self.merchant_person_feature[key][27] == 0:
                self.merchant_person_feature[key][42] = 0
            else:
                self.merchant_person_feature[key][42] = float(self.merchant_person_feature[key][9]) / self.merchant_person_feature[key][27]

            if self.merchant_person_feature[key][28] == 0:
                self.merchant_person_feature[key][43] = 0
            else:
                self.merchant_person_feature[key][43] = float(self.merchant_person_feature[key][10]) / self.merchant_person_feature[key][28]

            if self.merchant_person_feature[key][29] == 0:
                self.merchant_person_feature[key][44] = 0
            else:
                self.merchant_person_feature[key][44] = float(self.merchant_person_feature[key][11]) / self.merchant_person_feature[key][29]

            if self.merchant_person_feature[key][30] == 0:
                self.merchant_person_feature[key][45] = 0
            else:
                self.merchant_person_feature[key][45] = float(self.merchant_person_feature[key][12]) / self.merchant_person_feature[key][30]

            if self.merchant_person_feature[key][31] == 0:
                self.merchant_person_feature[key][46] = 0
            else:
                self.merchant_person_feature[key][46] = float(self.merchant_person_feature[key][13]) / self.merchant_person_feature[key][31]

            if self.merchant_person_feature[key][32] == 0:
                self.merchant_person_feature[key][47] = 0
            else:
                self.merchant_person_feature[key][47] = float(self.merchant_person_feature[key][14]) / self.merchant_person_feature[key][32]

            # 访问1次用户，2次用户，3次用户，3次以上用户
            person_count1 = 0
            person_count2 = 0
            person_count3 = 0
            person_count3plus = 0

            for person in self.merchant_person_times[key]['all'].keys():
                if self.merchant_person_times[key]['all'][person] == 1:
                    person_count1 += 1
                if self.merchant_person_times[key]['all'][person] == 2:
                    person_count2 += 1
                if self.merchant_person_times[key]['all'][person] == 3 :
                    person_count3 += 1
                if self.merchant_person_times[key]['all'][person] > 3 :
                    person_count3plus += 1

            self.merchant_person_feature[key][48] = person_count1
            self.merchant_person_feature[key][49] = person_count2
            self.merchant_person_feature[key][50] = person_count3
            self.merchant_person_feature[key][51] = person_count3plus

            if self.merchant_person_feature[key][9] == 0 :
                self.merchant_person_feature[key][52] = 0
                self.merchant_person_feature[key][53] = 0
                self.merchant_person_feature[key][54] = 0
                self.merchant_person_feature[key][55] = 0
            else:
                self.merchant_person_feature[key][52] = float(self.merchant_person_feature[key][48]) / self.merchant_person_feature[key][9]
                self.merchant_person_feature[key][53] = float(self.merchant_person_feature[key][49]) / self.merchant_person_feature[key][9]
                self.merchant_person_feature[key][54] = float(self.merchant_person_feature[key][50]) / self.merchant_person_feature[key][9]
                self.merchant_person_feature[key][55] = float(self.merchant_person_feature[key][51]) / self.merchant_person_feature[key][9]



    def mergeMerchantFeature(self, enddays):

        self.getMerchantid_dummycode()
        self.getMerchantAndLocation()
        self.getMerchantBasevalue(enddays)
        self.getMerchantDivvalue(enddays)

        print 'Merge the merchant feature ...'
        for key in self.merchant_person_feature.keys():
            if not self.koubei_merchant_feature.has_key(key):
                self.koubei_merchant_feature[key] = []

            self.koubei_merchant_feature[key].extend(self.merchantid_dummycode[key[0]])
            self.koubei_merchant_feature[key].append(len(self.merchant_locations[key[0]]))
            self.koubei_merchant_feature[key].append(len(self.location_merchants[key[1]]))
            self.koubei_merchant_feature[key].extend(self.merchant_time_feature[key])
            self.koubei_merchant_feature[key].extend(self.merchant_person_feature[key])


if __name__ == '__main__':

    kb = koubeiMerchantFeature()
    kb.mergeMerchantFeature(153)
    for key in kb.koubei_merchant_feature.keys():
        print 'pair',key, 'feature:',kb.koubei_merchant_feature[key]
    print 'the size:',len(kb.koubei_merchant_feature.keys())