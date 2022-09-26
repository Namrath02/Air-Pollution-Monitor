import matplotlib.pyplot as plt
import time
import datetime
import csv

x=[]
y=[]

with open('feeds.csv' , 'r') as csvfile:
    with open('newv.csv', 'w') as newfile:
        writer = csv.writer(newfile)
        plots = csv.reader(csvfile, delimiter=',')
        i=1
        for row in plots:
            if i==1:
                i=0
                continue
            tmp = row[0]
            # convert timestamp of format 2022-09-01T23:34:59+05:30 to datetime object
            # tmp = datetime.strptime(tmp, '%Y-%m-%dT%H:%M:%S%z')
            tmp = time.mktime(time.strptime(tmp, '%Y-%m-%dT%H:%M:%S%z'))
            row[0] = tmp
            i+=2
            # write this row to new csv
            print(row[0])
            if((row[0] > 1662645120.0) & (i%5==0)):
                writer.writerow(row)


