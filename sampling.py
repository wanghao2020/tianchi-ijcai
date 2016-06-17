import pickle
import random
import sys
import merge_traindata
import numpy as np

class sampling():

    # sampledata = {}
    # sampleFeature = []
    # sampleLabel = []
    # sampleUML = []

    def getsampledata(self):

        print "Load the train data set ....."
        mergedata = merge_traindata.mergetraindata()
        mergedata.getTomergetraindata()

        feature = mergedata.train_feature
        label = mergedata.train_label
        UMLpair = mergedata.train_UMLpair

        print "finsh loading data set and get the sample data ...."

        positive_sample = {}
        negative_sample = {}
        count = 0

        index = 0
        for i in range(len(label)):
            count += 1
            sys.stdout.write("\rsample count : %d" % count)
            sys.stdout.flush()
            if label[i] == 0:
                current_negative = feature[i]
                current_negative.append(0)
                negative_sample[UMLpair[index]] = current_negative
            else:
                current_positive = feature[i]
                current_positive.append(1)
                positive_sample[UMLpair[index]] = current_positive
            index += 1

        print "\r\npositive sample nums ", len(positive_sample)
        print "nagative sample nums ", len(negative_sample)

        sampledata = {}
        sampleFeature = []
        sampleLabel = []
        sampleUML = []

        for key in positive_sample.keys():
            sampledata[key] = positive_sample[key]

        for key in random.sample(negative_sample, len(positive_sample) * 10 ):
            sampledata[key] = negative_sample[key]


        count = 0
        for key in sampledata.keys():
            count += 1
            sys.stdout.write("\r result sample count %d" % count)
            sampleUML.append(key)
            sampleFeature.append(sampledata[key][0:-1])
            sampleLabel.append(sampledata[key][-1])

        print "Finsh the sample data Over ...."

        samplefeatureArray = np.asarray(sampleFeature)
        samplelabelArray = np.asarray(sampleLabel)

        return samplefeatureArray, samplelabelArray,sampleUML


        #print " write file ...."

        #outfile = open('/home/wanghao/Document/tianchi/trainset/samplefeaturefrom7to10.pkl', 'wb')
        #outfile1 = open('/home/wanghao/Document/tianchi/trainset/samplelabelfrom7to10.pkl', 'wb')
        #pickle.dump(result_feature, outfile)
        #pickle.dump(result_label, outfile1)

        #print "finsh sample data file"

if __name__ == '__main__':

    sam = sampling()
    samplefeature,samplelabel,sampleUML = sam.getsampledata()
    np.save('./samplefeature.npy',samplefeature)
    np.save('./samplelabel.npy',samplelabel)
    wfile = open('/home/wanghao/model/samplepair','wb')
    import csv
    writer = csv.writer(wfile)
    writer.writerows(sampleUML)
    wfile.close()
