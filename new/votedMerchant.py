# coding = utf-8
import pickle
import sys
import csv

class votedMerchant():

    merchant_budget = {}
    UL_Merchant_Matrix = {}
    endandzerocount = 0
    result = {}

    def getMerchantBudget(self):

        merchantfile = '/home/wanghao/model/ijcai2016_merchant_info'
        with open(merchantfile, 'rb') as f :
            for line in f :
                line = line.strip('\r\n')
                merchant,budget,locations = line.split(',')
                if not self.merchant_budget.has_key(merchant):
                    self.merchant_budget[merchant] = int(budget)

    def getFirstMerchant(self):

        merchant_votednum = {}
        merchant_user_prediction = {}
        self.endandzerocount = 0
        for key in self.UL_Merchant_Matrix.keys():

            merchant_prob_list = self.UL_Merchant_Matrix[key]

            failnum = 0
            for index in merchant_prob_list:
                m , pro ,tag = index
                if tag == -2:
                    self.endandzerocount += 1
                    break
                if tag == 0:
                    if not merchant_votednum.has_key(m):
                        merchant_votednum[m] = 0
                        merchant_user_prediction[m] = {}
                    merchant_votednum[m] += 1
                    merchant_user_prediction[m][key] = int(pro)
                    break
                if tag == -1 :
                    failnum += 1
            if failnum == len(merchant_prob_list):
                self.UL_Merchant_Matrix[key][0][2] = -2
                self.endandzerocount += 1

        sortedMerchantresult = sorted(merchant_votednum.iteritems(), key=lambda d:d[1],reverse=True)
        hot_merchant = sortedMerchantresult[0][0]

        sortedUserProb = sorted(merchant_user_prediction[hot_merchant].iteritems(),key=lambda d:d[1],reverse=True)
        resultUser = sortedUserProb[0:int(1.5*self.merchant_budget[hot_merchant])]

        for key in resultUser:
            if not self.result.has_key(key):
                self.result[key] = hot_merchant

        for key in merchant_user_prediction[hot_merchant].keys():

            successcount = 0
            for merchantlist in self.UL_Merchant_Matrix[key]:
                #merchant,pro,tag = merchantlist
                if merchantlist[0] == hot_merchant:
                    merchantlist[2] = 1
                if merchantlist[2] == 1:
                    successcount += 1
                if successcount == 2:
                    self.UL_Merchant_Matrix[key][0][2] = -2
                    break



    def getMerchant(self):
        print 'Load the UL_merchant matrix pkl ...'
        readfile1 = open('./UL_M_RateMatrix.pkl','rb')
        self.UL_Merchant_Matrix = pickle.load(readfile1)
        print 'Load the data over ...'
        self.getMerchantBudget()
        print '*'*50

        count = 0
        while(True):
            if self.endandzerocount == len(self.UL_Merchant_Matrix):
                print 'Recommendation over ...'
                break

            sys.stdout.write('\rcount %d'%count)
            sys.stdout.flush()
            self.getFirstMerchant()
            count += 1
            if count >= 5000:
                break



if __name__ == '__main__':

    voted = votedMerchant()
    voted.getMerchant()
    wfile = open('./result.csv','wb')
    writer = csv.writer(wfile)
    for key in voted.result.keys():
        result = []
        result.append(key[0])
        result.append(key[0])
        stringlist = ''
        for mer in voted.result[key]:
            stringlist = stringlist + mer +':'
        stringlist = stringlist[0:len(stringlist) - 1]
        result.append(result)
        writer.writerow(result)
    wfile.close()
