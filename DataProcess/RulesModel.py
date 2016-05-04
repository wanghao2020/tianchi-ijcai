from dataMethod import data
import csv
import random
from frequentItems import loc_rules

data = data()
# get the location_merchant_nums
data.get_location_merchant_nums()
location_merchant_nums = data.location_merchant_nums

# get the user_merchant_nums
data.input_train_data()
user_merchant_nums = data.user_merchant_nums

data.inputdata()
location_merchant = data.location_merchant
# load the test file
Allresult = []
testfile = data.koubeitest_path

with open(testfile,'rb') as f :
    for line  in f :
        result = []
        linelist = line[0:len(line)-1].split(',')
        user = linelist[0]
        location = linelist[1]

        result.append(user)
        result.append(location)

        merchantResult = []
        # add visited merchants
        if user_merchant_nums.has_key(user):
            for merchant in user_merchant_nums[user]:
                if location_merchant_nums.has_key(location):
                    if location_merchant_nums[location].has_key(merchant):
                        merchantResult.append(merchant)


        # result > 10
        if len(merchantResult) > 10 :
            count = 0
            mostFrequentMechantResult = []
            sortedMerchantlist = sorted(user_merchant_nums[user].iteritems(),key=lambda d:d[1],reverse=True)
            for merchant in sortedMerchantlist:
                if merchant[0] in merchantResult:
                    mostFrequentMechantResult.append(merchant[0])
                    count = count + 1
                    if count == 10 :
                        break
            string = ''
            for merchant in mostFrequentMechantResult:
                string = string + str(merchant) + ':'
            string = string[0:len(string)-1]
            result.append(string)
            Allresult.append(result)

        # add rules merchant
        rules_add = []
        rules_add_count = 0
        if user_merchant_nums.has_key(user):
            rules_add.append(user)
            rules_add.append(location)
            for merchant in user_merchant_nums[user]:
                #print 'location:',type(location),location
                #print loc_rules[location]
                if(loc_rules.has_key(location)):

                    rules_add_merchant = []
                    for merlist in loc_rules[location]:
                        if merchant in merlist[0]:
                            print "i am here"
                            for x in merlist[1]:
                                 rules_add_count += 1
                                 if(x not in merchantResult):
                                    merchantResult.append(x)
                                    rules_add_merchant.append(x)

            rules_add.append(rules_add_merchant)

            #print "rules add:",rules_add

        # merchant num < 3
        if location_merchant_nums.has_key(location):
            if len(location_merchant_nums[location]) < 3 :
                for key in location_merchant_nums[location]:
                    if(key not in merchantResult):
                        merchantResult.append(key)
                        if(len(merchantResult)>=10):
                            break
                merchantResult = set(merchantResult)
                string = ''
                for merchant in merchantResult:
                    string = string + str(merchant) + ':'
                string = string[0:len(string) - 1]
                result.append(string)
                Allresult.append(result)

            else:
                count = 0
                sortedMerchantlist = sorted(location_merchant_nums[location].iteritems(),key=lambda d:d[1],reverse=True)
                for merchant in sortedMerchantlist:
                    if merchant[0] not in merchantResult:
                        merchantResult.append(merchant[0])
                        count = count + 1
                        if count == 2 or len(merchantResult) >= 10 :
                            break
                string = ''
                for merchant in merchantResult:
                    string = string + str(merchant) + ':'
                string = string[0:len(string) - 1]
                result.append(string)
                Allresult.append(result)
        else:
            #print type(location),location
            merchantlist = location_merchant[location]
            if len(merchantlist) > 3 :
                merchantlist = random.sample(merchantlist,3)

            for merchant in merchantlist:
                merchantResult.append(merchant)

            string = ''
            for merchant in merchantResult:
                string = string + str(merchant) + ':'
            string = string[0:len(string) - 1]
            result.append(string)
            Allresult.append(result)
    print "rule_add_count",rules_add_count

#for result in Allresult:
#    print result
# write to the csv file
path = 'E:\IJCAI_competition\github_code\ijcai\DataProcess\submission2.csv'
with open(path,'wb') as f:
    writer = csv.writer(f)
    writer.writerows(Allresult)







