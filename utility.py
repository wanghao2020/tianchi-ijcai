import pickle
import numpy as np

file = '/home/wanghao/Document/tianchi/feature/sample.pkl'
f = open(file,'rb')
ary = pickle.load(f)
m,n = ary.shape

allnum = 0
positivenum = 0
negativenum = 0

for index in range(0,m):
    allnum += 1
    print ary[index]
    if ary[index][-1] == 1.0:
        positivenum += 1
    else:
        negativenum += 1

print "the ++++ nums ", positivenum
print "the ---- nums ", negativenum
print "all nums ", allnum




