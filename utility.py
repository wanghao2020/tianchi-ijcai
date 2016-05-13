import pickle
import csv
import numpy as np


# split the tianchi_merchant_train file by the time
def splitKoubeiDataBytime(starttime, endtime):

    file = "/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_koubei_train"
    writefile = '/home/wanghao/Document/tianchi/dataset/trainfrom%sto%s' % (starttime, endtime)
    print "-" * 50
    print "split the ijcal_koubei data set by time from %s to %s" % (starttime, endtime)

    wfile = open(writefile, 'wb')
    writer = csv.writer(wfile)
    with open(file,'rb') as f :
        for line in f :
            linedata = line.split(',')
            user = linedata[0]
            merchant = linedata[1]
            location = linedata[2]
            time = linedata[3]
            time = time[0:len(time)-1]
            if time >= starttime and time <= endtime :
                onelist = [user,merchant,location,time]
                writer.writerow(onelist)

    wfile.close()
    print "finsh the split data set by time from %s to %s" % (starttime, endtime)
    print "*" * 50

# split the taobao file by the time
def splitTaobaoDataBytime(starttime, endtime):

    file = '/home/wanghao/Document/tianchi/dataset/TaoBaoClean'
    writefile = '/home/wanghao/Document/tianchi/dataset/taobaofrom%sto%s' % (starttime, endtime)
    print "-"*50
    print "split the ijcal_taobao data set by time from %s to %s" %(starttime, endtime)

    count = 0
    wfile = open(writefile, 'wb')
    writer = csv.writer(wfile)
    with open(file, 'rb') as f:
        for line in f :
            line = line.strip('\r\n')
            user, seller, item, category, onlineAction, timeStamp = line.split(',')
            if timeStamp>= starttime and timeStamp<= endtime:
                onelist = [user, seller, item, category, onlineAction, timeStamp]
                writer.writerow(onelist)
            count += 1
            print count

    wfile.close()

    print "finsh the split data set by time from %s to %s" % (starttime, endtime)
    print "*"*50

if __name__ == "__main__":

    #splitTaobaoDataBytime('20150701', '20150930')
    #splitTaobaoDataBytime('20150701', '20151031')
    #splitKoubeiDataBytime('20151001', '20151031')
    #splitKoubeiDataBytime('20151101', '20151130')
    splitKoubeiDataBytime('20150701', '20150731')
    splitKoubeiDataBytime('20150801', '20150831')
    splitKoubeiDataBytime('20150901', '20150931')













