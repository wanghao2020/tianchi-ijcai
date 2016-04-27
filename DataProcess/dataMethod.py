import MySQLdb

# class for the data processing

class data :

    # file path
    file_path = '/home/wanghao/Document/tianchi/data_sets/'
    taobao_path = file_path + 'ijcai2016_taobao'
    merchantinfo_path = file_path + 'ijcai2016_merchant_info'
    koubeitrain_path = file_path + 'ijcai2016_koubei_train'
    koubeitest_path = file_path + 'ijcai2016_koubei_test'

    result_path = '/home/wanghao/Document/tianchi/result/result.csv'

    merchant_budget = {}
    location_merchant = {}
    location_merchant_nums = {}

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

    def get_location_merchant_nums(self):
        # process train file
        with open(self.koubeitrain_path) as f :
            for line in f :
                linelist = line.split(',')
                location = linelist[2]
                merchant = linelist[1]
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

        for dict in self.location_merchant_nums:
            print dict,self.location_merchant_nums[dict]


    def setdatapath(self,foldpath):

        self.file_path = foldpath
