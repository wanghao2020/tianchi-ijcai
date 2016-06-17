import sys
import csv
# get the location_ merchants data
merchantinfo = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_merchant_info'
location_merchants = {}
with open(merchantinfo, 'rb') as f :
    for line in f :
        line = line.strip('\r\n')
        merchant, budget, location = line.split(',')
        locations = location.split(':')
        for loc in locations :
            if not location_merchants.has_key(loc):
                location_merchants[loc] = []
            location_merchants[loc].append(merchant)


testfile = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_koubei_test'

LRtest = []
RFtest = []
with open(testfile, 'rb') as f:
    count = 0
    for line in f :
        count += 1
        sys.stdout.write('\rtest current count %d'%count)
        sys.stdout.flush()

        lrresult = []

        line = line.strip('\r\n')
        user,location = line.split(',')

        lrresult.append(user)
        lrresult.append(location)


        lrmerchants = ''

        for merchant in location_merchants[location]:
            lrmerchants = lrmerchants + merchant + ':'

        lrmerchants = lrmerchants[0:len(lrmerchants) - 1]

        lrresult.append(lrmerchants)

        LRtest.append(lrresult)

lrresultfile = '/home/wanghao/allresult.csv'


print "write the result to result file ...."


writefile1 = open(lrresultfile, 'wb')

write1 = csv.writer(writefile1)

write1.writerows(LRtest)
