import pickle

file = open('/home/wanghao/Document/tianchi/trainset/samplefrom7to10.pkl','rb')
d = pickle.load(file)
positivenum = 0
for i in range(len(d)):
    positivenum += d[i][-1]
print "positive sample num:", positivenum
print "negative sample num:", len(d)-positivenum