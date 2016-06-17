import pickle
import csv
import numpy as np
import datetime

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
    writefile = '/home/wanghao/Document/tianchi/dataset/taobaofrom%sto%s' % (int(starttime[4:6]), int(endtime[4:6]))
    print "-"*50
    print "split the ijcal_taobao data set by time from %s to %s" %(int(starttime[4:6]), int(endtime[4:6]))

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

def gettaobao11data():

    taobao10 = '/home/wanghao/Document/tianchi/dataset/taobao10'
    taobao11 = '/home/wanghao/Document/tianchi/dataset/taobaofrom11to11'
    new11 = '/home/wanghao/Document/tianchi/dataset/taobao11'
    wfile = open(new11, 'wb')
    writer = csv.writer(wfile)

    with open(taobao10,'rb') as f :
        for line in f :
            line = line.strip('\r\n')
            user,seller,item,category,action,time = line.split(',')
            if int(time[6:]) >= 12:
                formattime = datetime.datetime.strptime(time,'%Y%m%d')
                newtime = formattime + datetime.timedelta(days = 20)
                stringtime = newtime.strftime('%Y%m%d')
                onelist = [user,seller,item,category,action,stringtime]
                writer.writerow(onelist)
    print '11...'
    with open(taobao11, 'rb') as f:
        for line in f:
            line = line.strip('\r\n')
            user, seller, item, category, action, time = line.split(',')
            onelist = [user, seller, item, category, action, time]
            writer.writerow(onelist)
    wfile.close()

def gettaobaofrom7to10():

    taobao7 = '/home/wanghao/Document/tianchi/dataset/taobao7'
    taobao8 = '/home/wanghao/Document/tianchi/dataset/taobao8'
    taobao9 = '/home/wanghao/Document/tianchi/dataset/taobao9'
    taobao10 = '/home/wanghao/Document/tianchi/dataset/taobao10'
    taobao11 = '/home/wanghao/Document/tianchi/dataset/taobao11'

    newfile = '/home/wanghao/Document/tianchi/dataset/taobaofrom7to10'
    wfile = open(newfile, 'wb')
    writer = csv.writer(wfile)

    with open(taobao7, 'rb') as f:
        for line in f:
            line = line.strip('\r\n')
            user, seller, item, category, action, time = line.split(',')
            onelist = [user, seller, item, category, action, time]
            writer.writerow(onelist)
    with open(taobao8, 'rb') as f:
        for line in f:
            line = line.strip('\r\n')
            user, seller, item, category, action, time = line.split(',')
            onelist = [user, seller, item, category, action, time]
            writer.writerow(onelist)
    with open(taobao9, 'rb') as f:
        for line in f:
            line = line.strip('\r\n')
            user, seller, item, category, action, time = line.split(',')
            onelist = [user, seller, item, category, action, time]
            writer.writerow(onelist)
    with open(taobao10, 'rb') as f:
        for line in f:
            line = line.strip('\r\n')
            user, seller, item, category, action, time = line.split(',')
            onelist = [user, seller, item, category, action, time]
            writer.writerow(onelist)

    wfile.close()



def gettaobaofrom7to11():

    taobao7 = '/home/wanghao/Document/tianchi/dataset/taobao7'
    taobao8 = '/home/wanghao/Document/tianchi/dataset/taobao8'
    taobao9 = '/home/wanghao/Document/tianchi/dataset/taobao9'
    taobao10 = '/home/wanghao/Document/tianchi/dataset/taobao10'
    taobao11 = '/home/wanghao/Document/tianchi/dataset/taobao11'

    newfile = '/home/wanghao/Document/tianchi/dataset/taobaofrom7to11'
    wfile = open(newfile, 'wb')
    writer = csv.writer(wfile)

    with open(taobao7, 'rb') as f:
        for line in f:
            line = line.strip('\r\n')
            user, seller, item, category, action, time = line.split(',')
            onelist = [user, seller, item, category, action, time]
            writer.writerow(onelist)
    with open(taobao8, 'rb') as f:
        for line in f:
            line = line.strip('\r\n')
            user, seller, item, category, action, time = line.split(',')
            onelist = [user, seller, item, category, action, time]
            writer.writerow(onelist)
    with open(taobao9, 'rb') as f:
        for line in f:
            line = line.strip('\r\n')
            user, seller, item, category, action, time = line.split(',')
            onelist = [user, seller, item, category, action, time]
            writer.writerow(onelist)
    with open(taobao10, 'rb') as f:
        for line in f:
            line = line.strip('\r\n')
            user, seller, item, category, action, time = line.split(',')
            onelist = [user, seller, item, category, action, time]
            writer.writerow(onelist)
    with open(taobao11, 'rb') as f:
        for line in f:
            line = line.strip('\r\n')
            user, seller, item, category, action, time = line.split(',')
            onelist = [user, seller, item, category, action, time]
            writer.writerow(onelist)
    wfile.close()

def splittestfile():

    testfile = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_koubei_test'
    all_nums = 473533
    part1 = all_nums/3
    part2 = 2* all_nums / 3
    part1file = '/home/wanghao/Document/tianchi/dataset/testpart1'
    part2file = '/home/wanghao/Document/tianchi/dataset/testpart2'
    part3file = '/home/wanghao/Document/tianchi/dataset/testpart3'
    count = 1
    wfile1 = open(part1file, 'wb')
    wfile2 = open(part2file, 'wb')
    wfile3 = open(part3file, 'wb')
    writer1 = csv.writer(wfile1)
    writer2 = csv.writer(wfile2)
    writer3 = csv.writer(wfile3)
    with open(testfile, 'rb')as f:
        for line in f :
            line = line.strip('\r\n')
            user,location = line.split(',')
            line = [user,location]
            if count <= part1:
                writer1.writerow(line)
            elif count <= part2:
                writer2.writerow(line)
            else:
                writer3.writerow(line)
            count += 1
    wfile1.close()
    wfile2.close()
    wfile3.close()

if __name__ == "__main__":

    #splitTaobaoDataBytime('20150701', '20150930')
    #splitTaobaoDataBytime('20150701', '20151031')
    #splitKoubeiDataBytime('20151001', '20151031')
    #splitKoubeiDataBytime('20151101', '20151130')
    # splitKoubeiDataBytime('20150701', '20150731')
    # splitKoubeiDataBytime('20150801', '20150831')
    # splitKoubeiDataBytime('20150901', '20150931')
    # splitTaobaoDataBytime('20150701','20150731')
    # splitTaobaoDataBytime('20150801', '20150831')
    # splitTaobaoDataBytime('20150901', '20150931')
    # splitTaobaoDataBytime('20151001', '20151031')
    # splitTaobaoDataBytime('20151101', '20151131')
    # gettaobao11data()
    # gettaobaofrom7to10()
    # gettaobaofrom7to11()
    splittestfile()










