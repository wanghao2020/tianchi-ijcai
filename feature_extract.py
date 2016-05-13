#coding=utf-8
import pickle
#

class featureExtract():

    # ----------------------  Merchant Feature

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

        feature = [0] * 7
        featureavg = [0] * 6
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
        for m,loc in merchantLocationPassagerFlow.iteritems():
            if not result.has_key((m, loc)):
                result[(m ,loc)] = [7]
            for i in range(0,7):
                result[(m,loc)][i] = merchantLocationPassagerFlow[(m, loc)][i] / allMerchantlocationPassageFlow[loc][i]

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
                    result[(m, loc)][i] = merchantlocationPasseangeFlow[(m, loc)][i] / allmerchantPassangeFlow[m][i]

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
                result[loc][i] = merhantsPassenageFlow[loc][i] / merchantnumsLocation[loc]

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

            result[key][0] = frequentUser / allUser

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
                result[key][1] = frequentUser / allUser

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
                result[key][2] = frequentUser / allUser

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
                result[key][3] = frequentUser / allUser

        return result

    # ----------------- get user & merchant feature
    # 得到用户去所在地商家的次数，所有月的，平均每个月，近三个月次数，近三个月次数的增量
    def getUserMerchantLocationNums(self, starttime, endtime):

        file = '/home/wanghao/Document/tianchi/dataset/trainfrom%sto%s' % (str(starttime), str(endtime))
        result = {}
        with open(file, 'rb') as f:
            for line in f :
                line = line.strip('\r\n')
                user,merchant,location,time = line.split(',')

                if not result.has_key((user,merchant,location)):
                    result[(user,merchant,location)] = [0] * 7
                result[((user,merchant,location))][0] += 1

                if int(time[4:6]) == endtime - 2:
                    result[((user,merchant,location))][2] += 1
                elif int(time[4:6]) == endtime - 1:
                    result[((user, merchant, location))][3] += 1
                elif int(time[4:6]) == endtime:
                    result[((user, merchant, location))][4] += 1

        for key in result.keys():
            result[key][1] = result[key][0] / (endtime - starttime + 1.0)
            result[key][5] = result[key][3] - result[key][2]
            result[key][6] = result[key][4] - result[key][3]

        return result


    # 用户访问商家的天数
    # 所有月，平均月，近三个月
    def getUserMerchantLocationDay(self, starttime, endtime):

        pass




if __name__ == '__main__':

    f = featureExtract()
    feature1 = f.getAllMerchantPassenageFlow(7,10)
    print feature1

    feature2 = f.getMerchantofLocationPassenagerFlow(7, 10)
    print feature2

    feature3 = f.getMerchantPassenageFlowofLocation(7,10)
    print feature3
    print len(feature3)

    feature4 = f.getMerchantNumsofLocation()
    print feature4
    print len(feature4)

    feature5 = f.getMerchantBackPersonPercentage(7,10)
    print feature5
    print len(feature5)

    feature6 = f.getMerchantofMerchantsPercentage(7,10)
    print feature6