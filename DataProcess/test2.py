import pprint,pickle

file = open('E:\IJCAI_competition\datasets\datasets\user_feature_taobao_test.pkl','rb')

data = pickle.load(file)
pprint.pprint(data)