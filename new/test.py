# get the result ensemble

budgets = 0
with open('/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_merchant_info') as f :
    for line in f :
        line = line.strip('\r\n')
        merchant,budget,locations = line.split(',')
        budgets = budgets + int(budget)

print 'all budget ',budgets

merchantlist = []
with open('/home/wanghao/RFresult') as f :
    for line in f :
        line = line.strip('\r\n')
        user,location,merchant = line.split(',')
        merchants = merchant.split(':')
        for mer in merchants:
            merchantlist.append(mer)

print 'merhcant sizde ', len(merchantlist)