from dataMethod import data
import csv
import random

data = data()
# get the location_merchant_nums
data.get_location_merchant_nums()
location_merchant_nums = data.location_merchant_nums

# get the user_merchant_nums
data.input_train_data()
user_merchant_nums = data.user_merchant_nums

data.inputdata()
location_merchant = data.location_merchant
# load the test file
Allresult = []
testfile = data.koubeitest_path

print location_merchant['357']