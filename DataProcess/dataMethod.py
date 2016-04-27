#import MySQLdb
import numpy as np
import csv
# class for the data processing

class data :

    # file path
    file_path = 'E:\IJCAI_competition\datasets\datasets'
    taobao_path = file_path + '\ijcai2016_taobao'
    merchantinfo_path = file_path + '\ijcai2016_merchant_info'
    koubeitrain_path = file_path + '\ijcai2016_koubei_train'
    koubeitest_path = file_path + '\ijcai2016_koubei_test'

    #result_path = '/home/wanghao/Document/tianchi/result/result.csv'

    merchant_budget = {}
    location_merchant = {}
    user_merchant = {}
    user = {}
    merchant ={}
    user_sim = {}
    #seller_user_nums = {}

    def __init__(self):
        print "init"

    def inputdata(self):

        print "input the data ....."

        # Process the taobao

        #file = open(self.taobao_path,'r')
        #for line in file:
        #    print line

        # process the merchant file
        file = open(self.merchantinfo_path,'r')
        for line in file:
            linelist = line.split(',')
            self.merchant_budget.setdefault(int(linelist[0]),int(linelist[1]))

            locationlist = linelist[2].split(':')
            for location in locationlist:
                if self.location_merchant.has_key(int(location)):
                    self.location_merchant[int(location)].append(int(linelist[0]))
                else:
                    self.location_merchant[int(location)] = [int(linelist[0])]

        print ("the location nums is %d"%(len(self.location_merchant)))
        print ("the merchant nums is %d"%(len(self.merchant_budget)))

        #for dict in self.location_merchant:
         #   print dict
          #  print self.location_merchant.get(dict)


        # Process the train file


        # Process the test file

    def outputdata(self):
        print "output the result to csv"

    def setdatapath(self,foldpath):

        self.file_path = foldpath
    
    def input_train_data(self):
        file = open(self.koubeitrain_path,'r')
        i = 0
        for line in file:
            linelist = line.split(',')
            self.user[linelist[0]] = i
            i = i + 1
            temp_merchant_dict = {}
            if(self.user_merchant.has_key(linelist[0])):
                if(self.user_merchant[linelist[0]].has_key(linelist[1])):
                    self.user_merchant[linelist[0]][linelist[1]] = self.user_merchant[linelist[0]][linelist[1]] + 1
                else:
                    self.user_merchant[linelist[0]][linelist[1]] = 0
            else:
                temp_merchant_dict[linelist[1]] = 0
                self.user_merchant[linelist[0]] = temp_merchant_dict
            #self.user_merchant = sorted(self.user_merchant.iteritems(),key = lambda d:d[0])
        print('number of user:%d'%len(self.user))
        print('number of user_merchant:%d'%len(self.user_merchant))

    def input_merchant_data(self):
        file = open(self.merchantinfo_path,'r')
        j = 0
        for line in file:
            linelist1 = line.split(',')
            self.merchant[linelist1[0]] = j
            j = j + 1
        print('number of merchant:%d'%len(self.merchant))

    def Mer_Sim(self,d1,d2):
        keys1 = set(d1.keys())
        keys2 = set(d2.keys())
        return float((len(keys1&keys2)))/(len(keys1|keys2))

    def Comp_User_Sim(self):
        for usr_i in self.user_merchant:
            mer_dict_i = self.user_merchant[usr_i]
            self.user_sim[usr_i] = []
            for usr_j in self.user_merchant:
                mer_dict_j = self.user_merchant[usr_j]
                if(self.Mer_Sim(mer_dict_i,mer_dict_j)>0.5):
                    self.user_sim[usr_i].append(usr_j)
        result = []
        usr_count = []
        for usr in self.user_sim:
            usr_count.append(len(self.user_sim[usr]))
            res = usr + ','
            for usrs in self.user_sim[usr]:
                res = res + str(usrs) + ':'
            res = res[0:len(res)-1]
        result.append(res)
        csvfile = 'E:\IJCAI_competition\code\DataProcess\simi_usr.csv'
        with open(csvfile,'wb') as f:
            writer = csv.writer(f)
            writer.writerows(result)

        usr_count.sort(reversed = True)
        print(usr_count[1:5])
d = data()
#d.input_traindata()
  #  def input_taobao_data(self):
  #      file = open(self.taobao_path,'r')
d.input_train_data()
d.Comp_User_Sim()
