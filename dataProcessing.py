
# split the taobao data, get the user out that the user not in train file and test file

def splitTaoBaoData():

    taobaofile = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_taobao'
    trainfile = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_koubei_train'
    testfile = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_koubei_test'

    trainuser = set()
    testuser = set()

    with open(trainfile, 'rb') as f :
        for line in f :
            user, merchant, location, time = line.split(',')
            if user not in trainuser:
                trainuser.add(user)

    with open(testfile, 'rb') as f :
        for line in f :
            user, location= line.split(',')
            if user not in testuser:
                testuser.add(user)

    writefile = '/home/wanghao/Document/tianchi/dataset/TaoBaoClean'
    import csv
    wfile = open(writefile, 'wb')
    writer = csv.writer(wfile)

    with open(taobaofile, 'rb') as f :
        for line in f :
            user, seller, item ,cate , action,time = line.split(',')
            time = time[0:len(time) - 1]
            if user in trainuser or user in testuser:
                onelist = [user, seller, item, cate,action,time]
                print onelist
                writer.writerow(onelist)

    wfile.close()

if __name__ == '__main__':

    splitTaoBaoData()