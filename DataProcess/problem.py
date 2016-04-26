import MySQLdb
import csv

db = MySQLdb.connect(host="localhost",user="root",passwd="root",db="ijcal")

cursor = db.cursor()

cursor.execute("select count(*) from  merchant_info")

result = cursor.fetchall()

for row in result:
    print row

cursor.close()

db.close()


## test for the csv
csvfile = '/home/wanghao/Document/tianchi/result/result.csv'
with open (csvfile,'wb') as f :
    writer = csv.writer(f)
    data = [[1,1,'1:100'],[2,2,'2:200']]
    writer.writerows(data)




