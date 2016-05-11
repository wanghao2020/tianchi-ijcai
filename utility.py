import pickle
import csv
import numpy as np


# solit the tianchi_merchant_train file by the time
def splitDataSetBytime(starttime, endtime):
    file = "/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_koubei_train"
    splitdata = []
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
                splitdata.append(onelist)

    writefile = '/home/wanghao/Document/tianchi/dataset/trainfrom%sto%s'%(starttime, endtime)
    with open(writefile, 'wb') as f :
        writer = csv.writer(f)
        writer.writerows(splitdata)



if __name__ == "__main__":

    splitDataSetBytime('20150701', '20151031')













