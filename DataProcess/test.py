import csv
import random


from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
data = [[100,200,300],[500,600,70],[-100,-200,-300],[-5,-600,-700]]
target = [1,1,0,0]

x = preprocessing.scale(data)
print x
model = LogisticRegression(C =1 , penalty='l1',tol=0.001,max_iter=2000)
model.fit(x,target)

x = [[4,5,6],[-1,-2,-3]]
y_propred = model.predict_proba(x)
for y in y_propred:
    print y