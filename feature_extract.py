#coding=utf-8
import pickle
import datetime
from taobao_user_feature import taobao_user_feature
'''
Get the feature from the readme.docx
'''
class featureExtract():

    # month : [(uesr1, merchant1), (user1, merchant2)....]
    user_feature = {}
    user_taobao_feature = {}
    merchant_feature = {}
    userandmerchant_feature = {}
    location_merchant_nums = {}
    merchant_id_dummy_code = {}
    # ----------------------  Merchant Feature

    # merchant_id_dummy_code {merchant:str(code)}
    def Merchant_id_dummy_code(self):
        file = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_merchant_info'
        with open(file) as f:
            for line in f:
                line = line.strip('\r\n')
                merchant,budget,locationlist = line.split(',')
                if not self.merchant_id_dummy_code.has_key(merchant):
                    temp = bin(int(merchant)).replace('0b','')
                    zeros = ''
                    for i in range(14-len(temp)):
                        zeros += '0'
                    temp = zeros + temp
                    self.merchant_id_dummy_code[merchant] = [0] * 14
                    for i in range(14):
                        self.merchant_id_dummy_code[merchant][i] = temp[i]

    # def getMerchantIDFeature(self,starttime, endtime):
    #     result = {}
    #     file = '/home/wanghao/Document/tianchi/dataset/trainfrom%sto%s'%(str(starttime), str(endtime))
    #     with open(file, 'rb') as f :
    #         for line in f :
    #             line = line.strip('\r\n')
    #             user, m, location, time = line.split(',')
    #
    #             if not result.has_key(m):
    #                 result[m] = [0]*14
    #             for i in range(14):
    #                 result[m][i] = self.merchant_id_dummy_code[m][i]
    #     return result

    # all ; avg month ; 1, 2, 3,; 2,3 increase flow
    # 商家总店客流量；每个月客流量；近三个月客流量；近两个月增量
    def getAllMerchantPassenageFlow(self,starttime, endtime):

        result = {}
        file = '/home/wanghao/Document/tianchi/dataset/trainfrom%sto%s'%(str(starttime), str(endtime))
        with open(file, 'rb') as f :
            for line in f :
                line = line.strip('\r\n')
                user, m, location, time = line.split(',')

                if not result.has_key(m):
                    result[m] = [0]*7
                    # all
                result[m][0] += 1
                if int(time[4:6]) == endtime - 2:
                        # past 3
                    result[m][2] += 1
                elif int(time[4:6]) == endtime - 1:
                        # past 2
                    result[m][3] += 1
                elif int(time[4:6]) == endtime:
                        # past 1
                    result[m][4] += 1

        for m in result.keys():
            result[m][1] = result[m][0] / ((endtime - starttime + 1.0))
            result[m][5] = result[m][3] - result[m][2]
            result[m][6] = result[m][4] - result[m][3]

        return result

    # all passenagerflow, avg passenagerflow ,1, 2, 3 passenagerflow, 2,3 increase flow
    # avg day passenage flow; 1, 2, 3,avg day passenage flow; 2, 3 increase flow
    # 地点商家流量
    # 商家总流量，商家平均月流量，商家近三个月流量，近两个月增量
    def getMerchantofLocationPassenagerFlow(self, starttime, endtime):

        result = {}
        file = '/home/wanghao/Document/tianchi/dataset/trainfrom%sto%s' % (str(starttime), str(endtime))

        with open(file, 'rb') as f:
            for line in f:
                line = line.strip('\r\n')
                user, m, loc, time = line.split(',')
                if not result.has_key((m,loc)):
                    result[(m,loc)] = [0] * 13

                result[(m,loc)][0] += 1

                if int(time[4:6]) == endtime - 2:
                    result[(m, loc)][2] += 1
                elif int(time[4:6]) == endtime - 1:
                    result[(m, loc)][3] += 1
                elif int(time[4:6]) == endtime:
                    result[(m, loc)][4] += 1

        for key in result.keys():
            result[key][1] = result[key][0] / (endtime - starttime + 1.0)
            result[key][5] = result[key][3] - result[key][2]
            result[key][6] = result[key][4] - result[key][3]
            result[key][7] = result[key][0] / ((endtime - starttime + 1.0)*30)
            result[key][8] = result[key][2] / 30.0
            result[key][9] = result[key][3] / 30.0
            result[key][10] = result[key][4] /30.0
            result[key][11] = result[key][9] - result[key][8]
            result[key][12] = result[key][10] - result[key][9]

        return result


    # all merchant passanage flow ;avg month; 1, 2, 3 all flow, 2, 3 increase flow
    # 所在地所有商家客流量
    # 所有客流量，平均客流量，近三个月客流量，近两个月增量
    def getMerchantPassenageFlowofLocation(self, starttime, endtime):

        file = '/home/wanghao/Document/tianchi/dataset/trainfrom%sto%s' % (str(starttime), str(endtime))
        result = {}
        with open(file, 'rb') as f:
            for line in f :
                line = line.strip('\r\n')
                user,merchant,loc,time = line.split(',')
                if not result.has_key(loc):
                    result[loc] = [0] * 7
                result[loc][0] += 1
                if int(time[4:6]) == endtime - 2:
                        # past 3
                    result[loc][2] += 1
                elif int(time[4:6]) == endtime - 1:
                        # past 2
                    result[loc][3] += 1
                elif int(time[4:6]) == endtime:
                        # past 1
                    result[loc][4] += 1

        for key in result.keys():
            result[key][1] = float(result[key][0] / (endtime - starttime + 1.0))
            result[key][5] = result[key][3] - result[key][2]
            result[key][6] = result[key][4] - result[key][3]

        return result

    # merchant nums of the location
    # 所在地商家的数量
    def getMerchantNumsofLocation(self):

        # location : merchantNums
        location_merchant = {}
        file = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_merchant_info'
        with open(file, 'rb') as f :
            for line in f:
                line = line.strip('\r\n')
                merchant, budget, locations = line.split(',')
                for loc in locations.split(':'):
                    if not location_merchant.has_key(loc):
                        location_merchant[loc] = []
                    if merchant not in location_merchant[loc]:
                        location_merchant[loc].append(merchant)
        location_nums = {}
        for loc in location_merchant:
            location_nums[loc] = len(location_merchant[loc])

        return location_nums

    # merchant passange flow / all merchants passange flow
    # 地点商家分店所占该地的客流量比例：
    # 所有月，平均每个月，近三个月，近两个月增量
    def getMerchangPassenageFlowPercentageofLocation(self, starttime, endtime):

        merchantLocationPassagerFlow = self.getMerchantofLocationPassenagerFlow(starttime, endtime)
        allMerchantlocationPassageFlow = self.getMerchantPassenageFlowofLocation(starttime, endtime)

        result = {}
        for key in merchantLocationPassagerFlow.keys():
            if not result.has_key(key):
                result[key] = [0] * 7
            for i in range(0,7):
                if allMerchantlocationPassageFlow[key[1]][i] == 0 :
                    result[key][i] = -1
                else:
                    result[key][i] = float(merchantLocationPassagerFlow[key][i]) / allMerchantlocationPassageFlow[key[1]][i]

        return result


    # merchant get the all merchant percentage
    # 地点商家分店所占总店的客流量比例：
    # 所有月，平均每个月，近三个月，近两个月增量
    def getMerchantofMerchantsPercentage(self, starttime , endtime):

        merchantlocationPasseangeFlow = self.getMerchantofLocationPassenagerFlow(starttime, endtime)
        allmerchantPassangeFlow = self.getAllMerchantPassenageFlow(starttime, endtime)

        result = {}
        for m,loc in merchantlocationPasseangeFlow.keys():
            if not result.has_key((m, loc)):
                result[(m, loc)] = [0] * 7
            for i in range(7) :
                if allmerchantPassangeFlow[m][i] == 0 :
                    allmerchantPassangeFlow[m][i] = -1
                else:
                    result[(m, loc)][i] = float(merchantlocationPasseangeFlow[(m, loc)][i])/ allmerchantPassangeFlow[m][i]

        return result


    # location merchant avg passenage flow
    # 地点所有商家平均每个商家客流量
    # 所有月，平均月，近三个月，近两个月增量
    def getMerchantsAvgPassenageFlowofLocation(self, starttime, endtime):

        merhantsPassenageFlow = self.getMerchantPassenageFlowofLocation(starttime, endtime)
        merchantnumsLocation = self.getMerchantNumsofLocation()

        result = {}
        for loc in merhantsPassenageFlow.keys():
            if not result.has_key(loc):
                result[loc] = [0] * 7
            for i in range(7):
                result[loc][i] = float(merhantsPassenageFlow[loc][i]) / merchantnumsLocation[loc]

        return result

    # 访客率
    def getMerchantBackPersonPercentage(self, starttime, endtime):

        file = '/home/wanghao/Document/tianchi/dataset/trainfrom%sto%s' % (str(starttime), str(endtime))
        merchant_month_user = {}
        with open(file, 'rb') as f :
            for line in f :
                line = line.strip('\r\n')
                user,merchant,location,time = line.split(',')
                if not merchant_month_user.has_key((merchant, location)):
                    merchant_month_user[(merchant, location)] = {}
                    merchant_month_user[(merchant, location)]['all'] = {}
                    merchant_month_user[(merchant, location)]['pastone'] = {}
                    merchant_month_user[(merchant, location)]['pasttwo'] = {}
                    merchant_month_user[(merchant, location)]['past'] = {}

                if not merchant_month_user[(merchant, location)]['all'].has_key(user):
                    merchant_month_user[(merchant,location)]['all'][user] = 0

                merchant_month_user[(merchant, location)]['all'][user] += 1

                if int(time[4:6]) == endtime - 2:
                    if not merchant_month_user[(merchant, location)]['pastone'].has_key(user):
                        merchant_month_user[(merchant, location)]['pastone'][user] = 0
                    merchant_month_user[(merchant, location)]['pastone'][user] += 1
                elif int(time[4:6]) == endtime - 1:
                    if not merchant_month_user[(merchant, location)]['pasttwo'].has_key(user):
                        merchant_month_user[(merchant, location)]['pasttwo'][user] = 0
                    merchant_month_user[(merchant, location)]['pasttwo'][user] += 1
                elif int(time[4:6]) == endtime:
                    if not merchant_month_user[(merchant, location)]['past'].has_key(user):
                        merchant_month_user[(merchant, location)]['past'][user] = 0
                    merchant_month_user[(merchant, location)]['past'][user] += 1

        result = {}
        for key in merchant_month_user.keys():

            if not result.has_key(key):
                result[key] = [0] * 4

            # all back person
            frequentUser = 0.0
            allUser = 0
            for user in merchant_month_user[key]['all'].keys():
                allUser += 1
                if merchant_month_user[key]['all'][user] > 1:
                    frequentUser += 1
            if allUser:
                result[key][0] = float(frequentUser) / allUser
            else:
                result[key][0] = -1

            # past one back person
            frequentUser = 0.0
            allUser = 0
            for user in merchant_month_user[key]['pastone'].keys():
                allUser += 1
                if merchant_month_user[key]['pastone'][user] > 1:
                    frequentUser += 1
            if allUser == 0 :
                result[key][1] = -1
            else:
                result[key][1] = float(frequentUser) / allUser

            # past two back person
            frequentUser = 0.0
            allUser = 0
            for user in merchant_month_user[key]['pasttwo'].keys():
                allUser += 1
                if merchant_month_user[key]['pasttwo'][user] > 1:
                    frequentUser += 1

            if allUser == 0:
                result[key][2] = -1
            else:
                result[key][2] = float(frequentUser) / allUser

            # past back person
            frequentUser = 0.0
            allUser = 0
            for user in merchant_month_user[key]['past'].keys():
                allUser += 1
                if merchant_month_user[key]['past'][user] > 1:
                    frequentUser += 1

            if allUser == 0:
                result[key][3] = -1
            else:
                result[key][3] = float(frequentUser) / allUser

        return result

    def MergeMerchantFeature(self, starttime, endtime):

        # 1. 得到总店客流量, { merchant : feature * 7 }
        allmerchantFeature = self.getAllMerchantPassenageFlow(starttime, endtime)
        # 2. 地点商家客流量 { (merchant, location) : feature * 13 }
        merchantLocationPassenageFlow = self.getMerchantofLocationPassenagerFlow(starttime, endtime)
        # 3. 所在地所有商家客流量 {loc : feature * 7}
        locationMerchangPassenageFlow = self.getMerchantPassenageFlowofLocation(starttime, endtime)
        # 4. 所在地商家的数量 {loc : merchantnums}
        locationmerchantNums = self.getMerchantNumsofLocation()
        # 5. 所在地商家占该地客流量 { （merchant, location） : feature * 7}
        merchantlocationPersonFlowPercentage = self.getMerchangPassenageFlowPercentageofLocation(starttime,endtime)
        # 6. 分店占总店流量的比例 { (merchant,location) : feature}
        merchantofMerchantsPersonflowPercentage = self.getMerchantofMerchantsPercentage(starttime, endtime)
        # 7. 地点商家平均客流量 {loc : feature}
        locationMerchantAvgPersonflowPercentage = self.getMerchantsAvgPassenageFlowofLocation(starttime, endtime)
        # 8. 返客率 {（merchant, location） : feature }
        backpersonPercentage = self.getMerchantBackPersonPercentage(starttime, endtime)
        # 9. merchant id dummy code {merchant: id_feature * 14}

        for key in merchantLocationPassenageFlow.keys():
            if not self.merchant_feature.has_key(key):
                self.merchant_feature[key] = []
            self.merchant_feature[key].extend(allmerchantFeature[key[0]])
            self.merchant_feature[key].extend(merchantLocationPassenageFlow[key])
            self.merchant_feature[key].extend(locationMerchangPassenageFlow[key[1]])
            self.merchant_feature[key].append(locationmerchantNums[key[1]])
            self.merchant_feature[key].extend(merchantlocationPersonFlowPercentage[key])
            self.merchant_feature[key].extend(merchantofMerchantsPersonflowPercentage[key])
            self.merchant_feature[key].extend(locationMerchantAvgPersonflowPercentage[key[1]])
            self.merchant_feature[key].extend(backpersonPercentage[key])
            # 6. 用户访问的商家的id {merchant:id_feature *14}
            self.Merchant_id_dummy_code()
            self.merchant_feature[key].extend(self.merchant_id_dummy_code[key[0]])

    # ----------------- get user & merchant feature --------------------------
    # ------------------------------------------------------------------------

    # 得到用户去所在商家的次数，所有月的，平均每个月，近三个月次数，近三个月次数的增量
    def getUserMerchantLocationNums(self, starttime, endtime):

        file = '/home/wanghao/Document/tianchi/dataset/trainfrom%sto%s' % (str(starttime), str(endtime))
        result = {}
        with open(file, 'rb') as f:
            for line in f :
                line = line.strip('\r\n')
                user,merchant,location,time = line.split(',')

                if not result.has_key((user,merchant)):
                    result[(user,merchant)] = [0] * 7
                result[((user,merchant))][0] += 1

                if int(time[4:6]) == endtime - 2:
                    result[((user,merchant))][2] += 1
                elif int(time[4:6]) == endtime - 1:
                    result[((user, merchant))][3] += 1
                elif int(time[4:6]) == endtime:
                    result[((user, merchant))][4] += 1

        for key in result.keys():
            result[key][1] = result[key][0] / (endtime - starttime + 1.0)
            result[key][5] = result[key][3] - result[key][2]
            result[key][6] = result[key][4] - result[key][3]

        return result


    # 用户访问商家的天数
    # 所有月，平均月，近三个月,近三个月的增量,最长间隔，最短间隔，平均间隔
    def getUserMerchantLocationDay(self, starttime, endtime):

        file = '/home/wanghao/Document/tianchi/dataset/trainfrom%sto%s' % (str(starttime), str(endtime))
        UserMerchantLocation_time = {}
        with open(file, 'rb') as f:
            for line in f:
                line = line.strip('\r\n')
                user,merchant,location,time = line.split(',')
                if not UserMerchantLocation_time.has_key((user,merchant)):
                    UserMerchantLocation_time[(user,merchant)] = []
                if time not in UserMerchantLocation_time[(user,merchant)]:
                    UserMerchantLocation_time[(user,merchant)].append(time)

        result = {}
        for pair in UserMerchantLocation_time:
            if pair not in result:
                result[pair] = [0] * 10
            result[pair][0] = len(UserMerchantLocation_time[pair])
            result[pair][1] = result[pair][0] / (endtime - starttime + 1.0)
            for time in UserMerchantLocation_time[pair]:
                if int(time[4:6]) == endtime - 2:
                    result[pair][2] += 1
                elif int(time[4:6]) == endtime - 1:
                    result[pair][3] += 1
                elif int(time[4:6]) == endtime:
                    result[pair][4] += 1

            result[pair][5] = result[pair][3] - result[pair][2]
            result[pair][6] = result[pair][4] - result[pair][3]

            if len(UserMerchantLocation_time[pair]) <= 1:
                result[pair][7] = -1
                result[pair][8] = -1
                result[pair][9] = -1
            else:
                sortedtime = sorted(UserMerchantLocation_time[pair])
                diff_time = []
                for i in range(0,len(sortedtime)-1):
                    firstdate = datetime.datetime.strptime(sortedtime[i],'%Y%m%d')
                    seconddate = datetime.datetime.strptime(sortedtime[i+1], '%Y%m%d')
                    diff_time.append((seconddate-firstdate).days)
                result[pair][7] = max(diff_time)
                result[pair][8] = min(diff_time)
                result[pair][9] = float(sum(diff_time)) / len(diff_time)

        return result


    # 转化率特征
    # 用户访问商家A的次数 / 该地商家A的客流量
    # 总的次数， 平均次数，近三个月的次数， 近两个月增量
    def getUserMerchantPercentageofMerchantsPassangeFlow(self,starttime,endtime):

        file = '/home/wanghao/Document/tianchi/dataset/trainfrom%sto%s' % (str(starttime), str(endtime))
        merchantsPassenageFlow = self.getAllMerchantPassenageFlow(starttime, endtime)
        userMerchantlocation = self.getUserMerchantLocationNums(starttime, endtime)
        result = {}
        with open(file, 'rb') as f:
            for line in f:
                line = line.strip('\r\n')
                user, merchant,location,time = line.split(',')
                if not result.has_key((user,merchant)):
                    result[(user,merchant)] = [0] * 7
                for i in range(0,7):
                    if merchantsPassenageFlow[merchant][i] == 0:
                        result[(user, merchant)][i] = 0
                    else:
                        result[(user,merchant)][i] = float(userMerchantlocation[(user,merchant)][i]) \
                                                          / merchantsPassenageFlow[merchant][i]
        return result



    # 比值类特征， 用户访问该地商家A的天数 / 用户的线下活跃天数
    def getUserMerchantLocationDaysPercentage(self,starttime,endtime):

        user_merchant_days = self.getUserMerchantLocationDay(starttime, endtime)
        result = {}
        for pair in user_merchant_days:
            if not result.has_key(pair):
                result[pair] = [0] * 7

            if self.user_feature[pair[0]][16] == 0 :
                result[pair][0] = -1
            else:
                result[pair][0] = float(user_merchant_days[pair][0]) / self.user_feature[pair[0]][16]

            if self.user_feature[pair[0]][20] == 0:
                result[pair][1] = -1
            else:
                result[pair][1] = float(user_merchant_days[pair][1]) / self.user_feature[pair[0]][20]

            if self.user_feature[pair[0]][17] == 0:
                result[pair][2] = -1
            else:
                result[pair][2] = float(user_merchant_days[pair][2]) / self.user_feature[pair[0]][17]

            if self.user_feature[pair[0]][18] == 0:
                result[pair][3] = -1
            else:
                result[pair][3] = float(user_merchant_days[pair][3]) / self.user_feature[pair[0]][18]

            if self.user_feature[pair[0]][19] == 0:
                result[pair][4] = -1
            else:
                result[pair][4] = float(user_merchant_days[pair][4]) / self.user_feature[pair[0]][19]

            if self.user_feature[pair[0]][21] == 0:
                result[pair][5] = -1
            else:
                result[pair][5] = float(user_merchant_days[pair][5]) / self.user_feature[pair[0]][21]

            if self.user_feature[pair[0]][22] == 0:
                result[pair][6] = -1
            else:
                result[pair][6] = float(user_merchant_days[pair][6]) / self.user_feature[pair[0]][22]

        return result

    # 用户访问商家A的次数/ 用户线下活跃天数
    def getUserMerchantLocationCountsPercentage(self,starttime,endtime):

        user_merchant_counts = self.getUserMerchantLocationNums(starttime, endtime)
        result = {}
        for pair in user_merchant_counts:
            if not result.has_key(pair):
                result[pair] = [0] * 7

            if self.user_feature[pair[0]][16] == 0:
                result[pair][0] = -1
            else:
                result[pair][0] = float(user_merchant_counts[pair][0]) / self.user_feature[pair[0]][16]

            if self.user_feature[pair[0]][20] == 0:
                result[pair][1] = -1
            else:
                result[pair][1] = float(user_merchant_counts[pair][1]) / self.user_feature[pair[0]][20]

            if self.user_feature[pair[0]][17] == 0:
                result[pair][2] = -1
            else:
                result[pair][2] = float(user_merchant_counts[pair][2]) / self.user_feature[pair[0]][17]

            if self.user_feature[pair[0]][18] == 0:
                result[pair][3] = -1
            else:
                result[pair][3] = float(user_merchant_counts[pair][3]) / self.user_feature[pair[0]][18]

            if self.user_feature[pair[0]][19] == 0:
                result[pair][4] = -1
            else:
                result[pair][4] = float(user_merchant_counts[pair][4]) / self.user_feature[pair[0]][19]

            if self.user_feature[pair[0]][21] == 0:
                result[pair][5] = -1
            else:
                result[pair][5] = float(user_merchant_counts[pair][5]) / self.user_feature[pair[0]][21]

            if self.user_feature[pair[0]][22] == 0:
                result[pair][6] = -1
            else:
                result[pair][6] = float(user_merchant_counts[pair][6]) / self.user_feature[pair[0]][22]

        return result


    def mergeUserMerchantFeature(self, starttime, endtime):

        # 1. 用户去商家的次数 {(user,merchant,location) : feature}
        usermerchantCounts = self.getUserMerchantLocationNums(starttime, endtime)
        # 2. 用户访问商家的天数 {（user,merchant,location） : feature}
        usermerchantDays = self.getUserMerchantLocationDay(starttime, endtime)
        # 3. 用户访问商家的次数 / 商家的客流量  { （user.merchant,location） : feature}
        usermerchantCountofmerchants = self.getUserMerchantPercentageofMerchantsPassangeFlow(starttime, endtime)
        # 4. 用户访问商家的天数 / 用户活跃的天数
        usermerchantDayPercentage = self.getUserMerchantLocationDaysPercentage(starttime, endtime)
        # 5. 用户访问商家的次数 / 用户活跃的天数
        usermerchantCountsPercentage = self.getUserMerchantLocationCountsPercentage(starttime, endtime)

        for key in usermerchantCounts.keys():
            if not self.userandmerchant_feature.has_key(key):
                self.userandmerchant_feature[key] = []
            self.userandmerchant_feature[key].extend(usermerchantCounts[key])
            self.userandmerchant_feature[key].extend(usermerchantDays[key])
            self.userandmerchant_feature[key].extend(usermerchantCountofmerchants[key])
            self.userandmerchant_feature[key].extend(usermerchantDayPercentage[key])
            self.userandmerchant_feature[key].extend(usermerchantCountsPercentage[key])

    # ------------------------------------------- User Feature -----------------------

    # 得到用户去的过哪些地点 和 用户去商家的不同时间
    # get user_location {user:[loc1,loc2]}
    # get user_merchant_datetime {user:{merchant:[time1,time2...],..},...}
    def get_user_merchant_datetime(self, dataset):
        user_merchant_datetime = {}
        user_location = {}
        with open(dataset) as f:
            for line in f:
                line = line.strip('\r\n')
                user, merchant, location, time = line.split(',')

                # datetime ...
                if not user_merchant_datetime.has_key(user):
                    user_merchant_datetime[user] = {}
                if not user_merchant_datetime[user].has_key(merchant):
                    user_merchant_datetime[user][merchant] = []
                format_time = datetime.datetime.strptime(time, '%Y%m%d')
                user_merchant_datetime[user][merchant].append(format_time)

                # location ...
                if not user_location.has_key(user):
                    user_location[user] = []
                if location not in user_location[user]:
                    user_location[user].append(location)

        return user_merchant_datetime, user_location

    # 得到地点下商家的数量
    #  get the {location : { merchant : visted nums }}
    def get_location_merchant_nums(self, dataset):
        with open(dataset) as f:
            for line in f:
                line = line.strip('\r\n')
                user, merchant, location, time = line.split(',')

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

    # -------------------------------------user feature in koubei (55维)-----------------------------
    def get_user_feature(self, dataset, startmonth, endmonth):

        user_merchant_datetime_all, user_location_all = self.get_user_merchant_datetime(dataset)
        self.get_location_merchant_nums(dataset)

        user_merchant_datetime = {}
        user_location = {}
        i = 0
        for month in range(startmonth, endmonth + 1):
            if endmonth - month + 1 > 3:
                continue
            dataset_part = '/home/wanghao/Document/tianchi/dataset/train' + str(month)
            user_merchant_datetime[i] = {}
            user_location[i] = {}

            user_merchant_datetime[i], user_location[i] = self.get_user_merchant_datetime(dataset_part)
            i += 1
        for user in user_merchant_datetime_all:
            if not self.user_feature.has_key(user):
                self.user_feature[user] = [0] * 55  # ?
            # ------------------user feature in koubei-----------------------------------
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
            for i in range(len(active_days_all) - 1):
                diff_days.append((active_days_all[i + 1] - active_days_all[i]).days)
            if len(diff_days) > 0:
                # 3. user max diff days offline
                self.user_feature[user][23] = max(diff_days)
                # 4. user min diff days offline
                self.user_feature[user][24] = min(diff_days)
                # 5. user avg diff days offline
                self.user_feature[user][25] = float(sum(diff_days)) / len(diff_days)
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
            self.user_feature[user][4] = float(self.user_feature[user][0]) / (endmonth - startmonth + 1)
            self.user_feature[user][5] = float(self.user_feature[user][0]) / ((endmonth - startmonth + 1) * 30)
            # increment num
            self.user_feature[user][6] = self.user_feature[user][2] - self.user_feature[user][1]
            self.user_feature[user][7] = self.user_feature[user][3] - self.user_feature[user][2]

            self.user_feature[user][9] = visited_mer_nums[0]
            self.user_feature[user][10] = visited_mer_nums[1]
            self.user_feature[user][11] = visited_mer_nums[2]
            self.user_feature[user][12] = float(self.user_feature[user][8]) / (endmonth - startmonth + 1)
            self.user_feature[user][13] = float(self.user_feature[user][8]) / ((endmonth - startmonth + 1) * 30)
            # increment num
            self.user_feature[user][14] = self.user_feature[user][10] - self.user_feature[user][9]
            self.user_feature[user][15] = self.user_feature[user][11] - self.user_feature[user][10]

            self.user_feature[user][17] = active_days[0]
            self.user_feature[user][18] = active_days[1]
            self.user_feature[user][19] = active_days[2]
            self.user_feature[user][20] = float(self.user_feature[user][16]) / (endmonth - startmonth + 1)
            # increment num
            self.user_feature[user][21] = self.user_feature[user][18] - self.user_feature[user][17]
            self.user_feature[user][22] = self.user_feature[user][19] - self.user_feature[user][18]

            self.user_feature[user][27] = visited_loc_nums[0]
            self.user_feature[user][28] = visited_loc_nums[1]
            self.user_feature[user][29] = visited_loc_nums[2]
            self.user_feature[user][30] = float(self.user_feature[user][26]) / (endmonth - startmonth + 1)
            # increment num
            self.user_feature[user][31] = self.user_feature[user][28] - self.user_feature[user][27]
            self.user_feature[user][32] = self.user_feature[user][29] - self.user_feature[user][28]
            if self.user_feature[user][17]:
                self.user_feature[user][34] = float(self.user_feature[user][1]) / self.user_feature[user][17]
            else:
                self.user_feature[user][34] = -1
            if self.user_feature[user][18]:
                self.user_feature[user][35] = float(self.user_feature[user][2]) / self.user_feature[user][18]
            else:
                self.user_feature[user][35] = -1
            if self.user_feature[user][19]:
                self.user_feature[user][36] = float(self.user_feature[user][3]) / self.user_feature[user][19]
            else:
                self.user_feature[user][36] = -1
            if self.user_feature[user][20]:
                self.user_feature[user][37] = float(self.user_feature[user][4]) / self.user_feature[user][20]
            else:
                self.user_feature[user][37] = -1
            if self.user_feature[user][21]:
                self.user_feature[user][38] = float(self.user_feature[user][6]) / self.user_feature[user][21]
            else:
                self.user_feature[user][38] = -1
            if self.user_feature[user][22]:
                self.user_feature[user][39] = float(self.user_feature[user][7]) / self.user_feature[user][22]
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
                self.user_feature[user][52] = float(repeat_mer_nums[0] + repeat_mer_nums[1] + repeat_mer_nums[2]) / 3 / \
                                              self.user_feature[user][12]
            else:
                self.user_feature[user][52] = -1
            if self.user_feature[user][14]:
                self.user_feature[user][53] = float(repeat_mer_nums[1] - repeat_mer_nums[0]) / self.user_feature[user][
                    14]
            else:
                self.user_feature[user][53] = -1
            if self.user_feature[user][15]:
                self.user_feature[user][54] = float(repeat_mer_nums[2] - repeat_mer_nums[1]) / self.user_feature[user][
                    15]
            else:
                self.user_feature[user][54] = -1

            # ******************************** user  feature in koubei ****************************

            # -------------------------------- user feature in taobao -----------------------------

    def get_user_taobao_feature(self, startmonth, endmonth):
        taobao_U = taobao_user_feature()
        taobao_U_feature = {}
        taobao_path = '/home/wanghao/Document/tianchi/dataset/taobaofrom' + str(startmonth) + 'to' + str(endmonth)
        taobao_U.get_taobao_user_feature(taobao_path)
        taobao_U_feature[0] = taobao_U.user_taobao_feature
        i = 0
        for month in range(startmonth, endmonth + 1):
            if endmonth - month + 1 > 3:
                continue
            taobao_part = '/home/wanghao/Document/tianchi/dataset/taobao' + str(month)
            taobao_U_part = taobao_user_feature()
            taobao_U_part.get_taobao_user_feature(taobao_part)
            taobao_U_feature[i + 1] = taobao_U_part.user_taobao_feature
            i += 1

        for user in taobao_U_feature[0].keys():
            if not self.user_taobao_feature.has_key(user):
                self.user_taobao_feature[user] = [0] * 192  # 192维
            # 切片：总的、近三个月
            for i in range(len(taobao_U_feature)):
                # 点击、购买商品数、商品类别数、商家数
                self.user_taobao_feature[user][0+33*i] = taobao_U_feature[i][user][0]
                self.user_taobao_feature[user][1+33*i] = taobao_U_feature[i][user][1]
                self.user_taobao_feature[user][2+33*i] = taobao_U_feature[i][user][2]
                self.user_taobao_feature[user][3+33*i] = taobao_U_feature[i][user][3]
                self.user_taobao_feature[user][4+33*i] = taobao_U_feature[i][user][4]
                self.user_taobao_feature[user][5+33*i] = taobao_U_feature[i][user][5]
                # 线上活跃天数
                self.user_taobao_feature[user][6+33*i] = taobao_U_feature[i][user][6]
                # 线上活跃间隔时间
                self.user_taobao_feature[user][7+33*i] = taobao_U_feature[i][user][7]
                self.user_taobao_feature[user][8+33*i] = taobao_U_feature[i][user][8]
                self.user_taobao_feature[user][9+33*i] = taobao_U_feature[i][user][9]
                # 总的点击、购买次数
                self.user_taobao_feature[user][10+33*i] = taobao_U_feature[i][user][16]
                self.user_taobao_feature[user][11+33*i] = taobao_U_feature[i][user][17]
                # 购买商品数（类别数、商家数）/点击商品数（类别数、商家数）
                if self.user_taobao_feature[user][0+33*i]:
                    self.user_taobao_feature[user][12+33*i] = float(self.user_taobao_feature[user][1+33*i])/self.user_taobao_feature[user][0+33*i]
                else:
                    self.user_taobao_feature[user][12+33*i] = -1
                if self.user_taobao_feature[user][2+33*i]:
                    self.user_taobao_feature[user][13+33*i] = float(self.user_taobao_feature[user][3+33*i])/self.user_taobao_feature[user][2+33*i]
                else:
                    self.user_taobao_feature[user][13+33*i] = -1
                if self.user_taobao_feature[user][4+33*i]:
                    self.user_taobao_feature[user][14+33*i] = float(self.user_taobao_feature[user][5+33*i])/self.user_taobao_feature[user][4+33*i]
                else:
                    self.user_taobao_feature[user][14+33*i] = -1
                # 点击、购买商品总量（商品类别数、商家数）/线上活跃天数
                if self.user_taobao_feature[user][6+33*i]:
                    self.user_taobao_feature[user][15+33*i] = float(self.user_taobao_feature[user][0+33*i])/self.user_taobao_feature[user][6+33*i]
                    self.user_taobao_feature[user][16+33*i] = float(self.user_taobao_feature[user][1+33*i])/self.user_taobao_feature[user][6+33*i]
                    self.user_taobao_feature[user][17+33*i] = float(self.user_taobao_feature[user][2+33*i])/self.user_taobao_feature[user][6+33*i]
                    self.user_taobao_feature[user][18+33*i] = float(self.user_taobao_feature[user][3+33*i])/self.user_taobao_feature[user][6+33*i]
                    self.user_taobao_feature[user][19+33*i] = float(self.user_taobao_feature[user][4+33*i])/self.user_taobao_feature[user][6+33*i]
                    self.user_taobao_feature[user][20+33*i] = float(self.user_taobao_feature[user][5+33*i])/self.user_taobao_feature[user][6+33*i]
                else:
                    self.user_taobao_feature[user][15+33*i] = -1
                    self.user_taobao_feature[user][16+33*i] = -1
                    self.user_taobao_feature[user][17+33*i] = -1
                    self.user_taobao_feature[user][18+33*i] = -1
                    self.user_taobao_feature[user][19+33*i] = -1
                    self.user_taobao_feature[user][20+33*i] = -1

                # 重复点击(购买)商品数(商品类别数、商家数)/总的点击(购买)商品数(商品类别数、商家数)
                for j in range(6):
                    if self.user_taobao_feature[user][j+33*i]:
                        self.user_taobao_feature[user][21+j+33*i] = float(taobao_U_feature[i][user][10+j])/self.user_taobao_feature[user][j+33*i]
                    else:
                        self.user_taobao_feature[user][21+j+33*i] = -1

                # 点击(购买)商品数(商品类别数、商家数)/总的点击(购买)次数
                if self.user_taobao_feature[user][10+33*i]:
                    self.user_taobao_feature[user][27+33*i] = float(self.user_taobao_feature[user][0+33*i])/self.user_taobao_feature[user][10+33*i]
                    self.user_taobao_feature[user][29+33*i] = float(self.user_taobao_feature[user][2+33*i])/self.user_taobao_feature[user][10+33*i]
                    self.user_taobao_feature[user][31+33*i] = float(self.user_taobao_feature[user][4+33*i])/self.user_taobao_feature[user][10+33*i]
                else:
                    self.user_taobao_feature[user][27+33*i] = -1
                    self.user_taobao_feature[user][29+33*i] = -1
                    self.user_taobao_feature[user][31+33*i] = -1

                if self.user_taobao_feature[user][11+33*i]:
                    self.user_taobao_feature[user][28+33*i] = float(self.user_taobao_feature[user][1+33*i])/self.user_taobao_feature[user][11+33*i]
                    self.user_taobao_feature[user][30+33*i] = float(self.user_taobao_feature[user][3+33*i])/self.user_taobao_feature[user][11+33*i]
                    self.user_taobao_feature[user][32+33*i] = float(self.user_taobao_feature[user][5+33*i])/self.user_taobao_feature[user][11+33*i]
                else:
                    self.user_taobao_feature[user][28+33*i] = -1
                    self.user_taobao_feature[user][30+33*i] = -1
                    self.user_taobao_feature[user][32+33*i] = -1

            # 切片：平均每个月
            # 点击、购买商品数、商品类别数、商家数
            for i in range(6):
                self.user_taobao_feature[user][132+i] = float(self.user_taobao_feature[user][0+i])/(endmonth-startmonth+1)

            # 线上活跃天数
            self.user_taobao_feature[user][138] = float(self.user_taobao_feature[user][6])/(endmonth-startmonth+1)
            # 点击、购买次数
            self.user_taobao_feature[user][139] = float(self.user_taobao_feature[user][10])/(endmonth-startmonth+1)
            self.user_taobao_feature[user][140] = float(self.user_taobao_feature[user][11])/(endmonth-startmonth+1)
            # 购买商品数（类别数、商家数）/点击商品数（类别数、商家数）
            self.user_taobao_feature[user][141] = float(self.user_taobao_feature[user][12])/(endmonth-startmonth+1)
            self.user_taobao_feature[user][142] = float(self.user_taobao_feature[user][13])/(endmonth-startmonth+1)
            self.user_taobao_feature[user][143] = float(self.user_taobao_feature[user][14])/(endmonth-startmonth+1)
            # 点击、购买商品总量（商品类别数、商家数）/线上活跃天数
            for i in range(6):
                self.user_taobao_feature[user][144+i] = float(self.user_taobao_feature[user][15+i])/(endmonth-startmonth+1)

            # 重复点击(购买)商品数(商品类别数、商家数)/总的点击(购买)商品数(商品类别数、商家数)
            for i in range(6):
                self.user_taobao_feature[user][150+i] = float(self.user_taobao_feature[user][21+i])/(endmonth-startmonth+1)

            # 点击(购买)商品数(商品类别数、商家数)/总的点击(购买)次数
            for i in range(6):
                self.user_taobao_feature[user][156+i] = float(self.user_taobao_feature[user][27+i])/(endmonth-startmonth+1)


            # 切片：增量
            # 点击、购买商品数、商品类别数、商家数
            j = 0
            for i in range(6):
                self.user_taobao_feature[user][132+j] = self.user_taobao_feature[user][0+i+33*2] - self.user_taobao_feature[user][0+i+33]
                self.user_taobao_feature[user][133+j] = self.user_taobao_feature[user][0+i+33*3] - self.user_taobao_feature[user][0+i+33*2]
                j += 2
            # 线上活跃天数
            self.user_taobao_feature[user][144] = self.user_taobao_feature[user][6+33*2] - self.user_taobao_feature[user][6+33]
            self.user_taobao_feature[user][145] = self.user_taobao_feature[user][6+33*3] - self.user_taobao_feature[user][6+33*2]
             # 点击、购买次数
            self.user_taobao_feature[user][146] = self.user_taobao_feature[user][10+33*2] - self.user_taobao_feature[user][10+33]
            self.user_taobao_feature[user][147] = self.user_taobao_feature[user][10+33*3] - self.user_taobao_feature[user][10+33*2]
            self.user_taobao_feature[user][148] = self.user_taobao_feature[user][11+33*2] - self.user_taobao_feature[user][11+33]
            self.user_taobao_feature[user][149] = self.user_taobao_feature[user][11+33*3] - self.user_taobao_feature[user][11+33*2]
            # 购买商品数（类别数、商家数）/点击商品数（类别数、商家数）
            j = 0
            for i in range(3):
                self.user_taobao_feature[user][150+j] = self.user_taobao_feature[user][12+i+33*2] - self.user_taobao_feature[user][12+i+33]
                self.user_taobao_feature[user][151+j] = self.user_taobao_feature[user][12+i+33*3] - self.user_taobao_feature[user][12+i+33*2]
                j += 2
            # 点击、购买商品总量（商品类别数、商家数）/线上活跃天数
            j = 0
            for i in range(6):
                self.user_taobao_feature[user][156+j] = self.user_taobao_feature[user][15+i+33*2] - self.user_taobao_feature[user][15+i+33]
                self.user_taobao_feature[user][157+j] = self.user_taobao_feature[user][15+i+33*3] - self.user_taobao_feature[user][15+i+33*2]
                j += 2
            # 重复点击(购买)商品数(商品类别数、商家数)/总的点击(购买)商品数(商品类别数、商家数)
            j = 0
            for i in range(6):
                self.user_taobao_feature[user][168+j] = self.user_taobao_feature[user][21+i+33*2] - self.user_taobao_feature[user][21+i+33]
                self.user_taobao_feature[user][169+j] = self.user_taobao_feature[user][21+i+33*3] - self.user_taobao_feature[user][21+i+33*2]
                j += 2
            # 点击(购买)商品数(商品类别数、商家数)/总的点击(购买)次数
            j = 0
            for i in range(6):
                self.user_taobao_feature[user][180+j] = self.user_taobao_feature[user][27+i+33*2] - self.user_taobao_feature[user][27+i+33]
                self.user_taobao_feature[user][181+j] = self.user_taobao_feature[user][27+i+33*3] - self.user_taobao_feature[user][27+i+33*2]
                j += 2


if __name__ == '__main__':

    f = featureExtract()
    f.Merchant_id_dummy_code()
    print "the dummy code : ",f.merchant_id_dummy_code['8']
    # f.get_user_feature('/home/wanghao/Document/tianchi/dataset/trainfrom7to10',7,10)
    # print len(f.user_feature['1027765'])
    # f.MergeMerchantFeature(7,10)
    # print  len(f.merchant_feature[('4822','172')])
    # f.mergeUserMerchantFeature(7,10)
    # print  len(f.userandmerchant_feature[('1027765','4822', '172')])
    # f.get_user_taobao_feature(7,10)