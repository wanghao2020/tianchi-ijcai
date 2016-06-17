import datetime
import csv
def taobao_time_format(filename,outfile):
    ofile = open(outfile,'wb')
    writer = csv.writer(ofile)
    with open(filename,'rb') as f:
        for line in f:
            line = line.strip('\r\n')

            user,seller,item,category,action,time = line.split(',')
            result = [user,seller,item,category,action]
            format_time = datetime.datetime.strptime(time,'%Y%m%d')
            start_time = '20150701'
            format_start_time = datetime.datetime.strptime(start_time,'%Y%m%d')
            duration = (format_time-format_start_time).days + 1
            result.append(duration)
            writer.writerow(result)
    ofile.close()

def train_time_format(filename,outfile):
    ofile = open(outfile,'wb')
    writer = csv.writer(ofile)
    with open(filename,'rb') as f:
        for line in f:
            line = line.strip('\r\n')

            user,merchant,location,time = line.split(',')
            result = [user,merchant,location]
            format_time = datetime.datetime.strptime(time,'%Y%m%d')
            start_time = '20150701'
            format_start_time = datetime.datetime.strptime(start_time,'%Y%m%d')
            duration = (format_time-format_start_time).days + 1
            result.append(duration)
            writer.writerow(result)
    ofile.close()

if __name__ == '__main__':
    # for i in range(7,12):
    #
    #     file = "/home/wanghao/Document/tianchi/dataset/taobao" + str(i)
    #     outfile = "/home/wanghao/Document/tianchi/dataset/dataset_t/taobao" + str(i) +'_t'
    #     taobao_time_format(file,outfile)
    #
    #     file2 = "/home/wanghao/Document/tianchi/dataset/train" + str(i)
    #     outfile2 = "/home/wanghao/Document/tianchi/dataset/dataset_t/train" + str(i) + '_t'
    #     train_time_format(file2, outfile2)
    #
    # file = "/home/wanghao/Document/tianchi/dataset/TaoBaoClean"
    # outfile = "/home/wanghao/Document/tianchi/dataset/dataset_t/TaoBaoClean_t"
    # taobao_time_format(file,outfile)
    # for i in range(10, 12):
    #     file = "/home/wanghao/Document/tianchi/dataset/taobaofrom7to" + str(i)
    #     outfile = "/home/wanghao/Document/tianchi/dataset/dataset_t/taobaofrom7to" + str(i) +'_t'
    #     taobao_time_format(file,outfile)
    #     file2 = "/home/wanghao/Document/tianchi/dataset/trainfrom7to" + str(i)
    #     outfile2 = "/home/wanghao/Document/tianchi/dataset/dataset_t/trainfrom7to" + str(i) + '_t'
    #     train_time_format(file2, outfile2)
    # file3 = "/home/wanghao/Document/tianchi/dataset/trainfrom7to9"
    # outfile3 = "/home/wanghao/Document/tianchi/dataset/dataset_t/trainfrom7to9_t"
    # train_time_format(file3, outfile3)

    file = "/home/wanghao/Document/tianchi/dataset/taobaofrom11to11"
    outfile = "/home/wanghao/Document/tianchi/dataset/dataset_t/taobaofrom11to11_t"
    taobao_time_format(file, outfile)