# get the result ensemble
import csv
def ensemble():
    modelresult1 = '/home/wanghao/RFresult_prediction.csv'
    modelresult2 = '/home/wanghao/RFsample1to5result_prediction.csv'
    ensembleresult = '/home/wanghao/ensembleprediction_7_3.csv'

    readfile1 = open(modelresult1, 'rb')
    readfile2 = open(modelresult2, 'rb')
    writerfile = open(ensembleresult, 'wb')

    writer = csv.writer(writerfile)
    data1 = readfile1.readlines()
    data2 = readfile2.readlines()

    lines = len(data1)

    for i in range(lines):

        result = []

        result1 = data1[i].strip('\r\n')
        result2 = data2[i].strip('\r\n')

        user_loc1,merchantproblists,s1 = result1.split('\"')
        user_loc1 = user_loc1[0:len(user_loc1) - 1]
        user1,loc1= user_loc1.split(',')

        merchantproblists = merchantproblists[0: len(merchantproblists) - 1]
        merchant_probs = merchantproblists.split(',')
        merchant_prob_dict1 = {}
        for term in merchant_probs:
            term = term.strip()
            merchant, prob = term.split(':')
            merchant = merchant.strip()
            if not merchant_prob_dict1.has_key(merchant):
                merchant_prob_dict1[merchant] = prob

        user_loc2, merchantproblists, s2 = result2.split('\"')
        user2, loc2, s2 = user_loc2.split(',')

        merchantproblists = merchantproblists[0 : len(merchantproblists) - 1]
        merchant_prob2 = merchantproblists.split(',')
        merchant_prob_dict2 = {}
        for term in merchant_prob2:
            term = term.strip()
            merchant, prob = term.split(':')
            merchant = merchant.strip()
            if not merchant_prob_dict2.has_key(merchant):
                merchant_prob_dict2[merchant] = prob

        sum_merchant_prob_dict = {}


        for mer in merchant_prob_dict1.keys():
            mer = mer.strip()
            sum_merchant_prob_dict[mer] = 0.7 * float(merchant_prob_dict1[mer]) + 0.3 * float(merchant_prob_dict2[mer])

        sorted_sum_merchant_prob = sorted(sum_merchant_prob_dict.iteritems(),key = lambda d:d[1],reverse=True)
        result.append(user1)
        result.append(loc1)
        stringlist = ''
        for key in sorted_sum_merchant_prob:
            stringlist = stringlist + key[0] + ':' + str(key[1]) + ','

        result.append(stringlist)
        writer.writerow(result)

    writerfile.close()


def pickout_result():
    maxcount = 0
    ensembleresult = open('/home/wanghao/RFresultprediction.csv','rb')
    outfile = open('/home/wanghao/RFresult','wb')
    writer = csv.writer(outfile)
    data = ensembleresult.readlines()
    result_count = [0]*11
    for i in range(len(data)):
        print i
        result = []
        count = 0
        line = data[i].strip('\r\n')
        user_loc, merchantproblist, s = line.split('\"')
        user, loc, s = user_loc.split(',')

        merchantproblist = merchantproblist[0:len(merchantproblist) - 1]
        merchant_prob = merchantproblist.split(',')
        merchant_prob_dict = {}
        for term in merchant_prob:
            term = term.strip()
            #print term
            merchant, prob = term.split(':')
            merchant = merchant.strip()
            if not merchant_prob_dict.has_key(merchant):
                merchant_prob_dict[merchant] = prob
        sorted_result = sorted(merchant_prob_dict.iteritems(),key=lambda  d:d[1],reverse=True)
        if len(sorted_result) > maxcount:
            maxcount = len(sorted_result)
        stringlist = ''
        for key in sorted_result:
            if float(key[1]) > 0.35:
                stringlist = stringlist + key[0] + ':'
                count += 1
            if count >=2:
                break
        stringlist = stringlist[0:len(stringlist) - 1]

        if count < 10:
            result_count[count] += 1
        else:
            result_count[10] += 1
        result.append(user)
        result.append(loc)
        result.append(stringlist)
        writer.writerow(result)

    for i in range(11):
        print "rec count:",i,",num:",result_count[i]
    print 'all merchant prediction', maxcount

if __name__ == '__main__':
    #ensemble()
    pickout_result()