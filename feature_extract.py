import pickle
#

class featureExtract():

    # month : [(uesr1, merchant1), (user1, merchant2)....]
    month_usermerchanttuple = {}

    def getMonthUserMerchantTuper(self, file, month):

        if not self.month_usermerchanttuple.has_key(month):
            self.month_usermerchanttuple[month] = []

        with open(file, 'rb') as f:
            count = 0
            for line in f :

                user, merchant, location, timstamp = line.split(',')
                tuple = (user, merchant)
                if tuple not in self.month_usermerchanttuple[month]:
                    self.month_usermerchanttuple[month].append(tuple)
                count += 1
                print count

        outfile = '/home/wanghao/Document/tianchi/dataset/userandmerchantTuple.pkl'
        with open(outfile, 'wb') as f :
            pickle.dump(self.month_usermerchanttuple, f)



if __name__ == '__main__':


    file = '/home/wanghao/Document/tianchi/dataset/trainfrom20151101to20151130'
    f  = featureExtract()
    f.getMonthUserMerchantTuper(file, '11')
    for tuple in f.month_usermerchanttuple['11']:
        print tuple
