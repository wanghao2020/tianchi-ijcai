# -*- coding: utf-8 -*-
import theano
import theano.tensor as T
import numpy as np
from sklearn import datasets
import matplotlib.pyplot as plt
import time
#定义数据类型

np.random.seed(0)
train_X, train_y = datasets.make_moons(300, noise=0.20)
train_X = train_X.astype(np.float32)
train_y = train_y.astype(np.int32)
num_example=len(train_X)

#设置参数
nn_input_dim = 332 #输入神经元个数
nn_output_dim = 2 #输出神经元个数
nn_hdim=100
#梯度下降参数
epsilon=0.01 #learning rate
reg_lambda=0.01 #正则化长度


#设置共享变量

w1=theano.shared(np.random.randn(nn_input_dim,nn_hdim),name="W1")
b1=theano.shared(np.zeros(nn_hdim),name="b1")
w2=theano.shared(np.random.randn(nn_hdim,nn_output_dim),name="W2")
b2=theano.shared(np.zeros(nn_output_dim),name="b2")

#前馈算法
X=T.matrix('X')  #double类型的矩阵
y=T.lvector('y') #int64类型的向量
z1=X.dot(w1)+b1
a1=T.tanh(z1)
z2=a1.dot(w2)+b2
y_hat=T.nnet.softmax(z2)
#正则化项
loss_reg=1./num_example * reg_lambda/2 * (T.sum(T.square(w1))+T.sum(T.square(w2)))
loss=T.nnet.categorical_crossentropy(y_hat,y).mean()+loss_reg
#预测结果
prediction=T.argmax(y_hat,axis=1)

forword_prop=theano.function([X],y_hat)
calculate_loss=theano.function([X,y],loss)
predict=theano.function([X],prediction)


#求导
dw2=T.grad(loss,w2)
db2=T.grad(loss,b2)
dw1=T.grad(loss,w1)
db1=T.grad(loss,b1)

#更新值
gradient_step=theano.function(
    [X,y],
    updates=(
        (w2,w2-epsilon*dw2),
        (b2,b2-epsilon*db2),
        (w1,w1-epsilon*dw1),
        (b1,b1-epsilon*db1)

    )
)

def build_model(num_passes=20000,print_loss=False):

    w1.set_value(np.random.randn(nn_input_dim, nn_hdim) / np.sqrt(nn_input_dim))
    b1.set_value(np.zeros(nn_hdim))
    w2.set_value(np.random.randn(nn_hdim, nn_output_dim) / np.sqrt(nn_hdim))
    b2.set_value(np.zeros(nn_output_dim))

    for i in xrange(0,num_passes):
        gradient_step(train_X,train_y)
        if print_loss and i%1000==0:
            print "Loss after iteration %i: %f" %(i,calculate_loss(train_X,train_y))
def accuracy_rate():
    predict_result=predict(train_X)
    count=0;
    for i in range(len(predict_result)):
        realResult=train_y[i]
        if(realResult==predict_result[i]):
            count+=1
    print "the correct rate is :%f" %(float(count)/len(predict_result))

def plot_decision_boundary(pred_func):
    # Set min and max values and give it some padding
    x_min, x_max = train_X[:, 0].min() - .5, train_X[:, 0].max() + .5
    y_min, y_max = train_X[:, 1].min() - .5, train_X[:, 1].max() + .5
    h = 0.01
    # Generate a grid of points with distance h between them
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    # Predict the function value for the whole gid
    Z = pred_func(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    # Plot the contour and training examples
    plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral)
    plt.scatter(train_X[:, 0], train_X[:, 1], c=train_y, cmap=plt.cm.Spectral)
    plt.show()


build_model(print_loss=True)
accuracy_rate()
# # plot_decision_boundary(lambda x: predict(x))
# # plt.title("Decision Boundary for hidden layer size 3")
