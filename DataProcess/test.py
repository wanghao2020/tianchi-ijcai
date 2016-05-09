from dataMethod import data
import csv
import random

merchantfile = '/home/wanghao/Document/tianchi/data_sets/ijcai2016_merchant_info'
location_merchant_nums = 0
with open(merchantfile, 'rb') as f:
    for line in f:
        merchant, budget, locationlists = line.split(',')
        locationlist = locationlists.split(':')
        for location in locationlist:
            print location