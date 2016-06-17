# coding=utf-8

import numpy as np
import random

class samping():



    def getSampledFeature(self, ratio):

        sample_UML = []

        trainpositivefeature = np.load('./trainpositivefeature.npy')
        trainpositive_UML = []
        with open('./trainpositiveUML','rb') as f :
            for line in f :
                line = line.strip('\r\n')
                user, merchant, location = line.split(',')
                trainpositive_UML.append((user,merchant,location))

        trainnegativefeature = np.load('./trainnegativefeature.npy')
        trainnegative_UML = []
        with open('./trainnegativeUML', 'rb') as f :
            for line in f :
                line = line.strip('\r\n')
                user, merchant, location = line.split(',')
                trainnegative_UML.append((user, merchant, location))

        positivecount = trainpositivefeature.shape[0]
        negativeCount = trainnegativefeature.shape[0]
        randomIndex = random.sample(range(negativeCount), positivecount * ratio)

        # 将两者累加即可
        sampledata = np.zeros(((ratio+1)*positivecount, 333))
        samplefeature = np.zeros(((ratio+1)*positivecount, 332))
        samplelabel = np.zeros((ratio+1)*positivecount)

        index = 0
        for i in range(positivecount):
            sampledata[index, 0:332] = trainpositivefeature[i,:]
            sampledata[index,-1] = 1
            index += 1

        for i in range(len(randomIndex)):
            sampledata[index,0:322] = trainnegativefeature[randomIndex[i], :]
            sampledata[index,-1] = 0
            index += 1

        np.random.shuffle(sampledata)
        samplefeature = sampledata[:,0:332]
        samplelabel = sampledata[:,-1]

        print 'the positive count size is : ',positivecount
        print 'the sample feature count size is :', samplefeature.shape
        print 'sample label label count size is :', samplelabel.shape

        print '*'*50
        print 'Save the sample feature ...'
        np.save('./samplefeature1to%d'%(ratio), samplefeature)
        print 'save the sample label ...'
        np.save('./samplelabel1to%d'%(ratio), samplelabel)



if __name__ == '__main__':

    sam = samping()
    sam.getSampledFeature(5)