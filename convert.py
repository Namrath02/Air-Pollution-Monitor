import matplotlib.pyplot as plt
import time
from collections import defaultdict
import csv
import numpy as np

# convert the format 2022-09-01T23:37:22+05:30 to 08 Sep 2022 18:34

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
            # convert timestamp of format 2022-09-01T23:34:59+05:30 to 08 Sep 2022 19:23
            if ((time.mktime(time.strptime(tmp, '%Y-%m-%dT%H:%M:%S%z'))>1662645120.0) & (i%5==0)):
                tmp = time.strftime('%d %b %Y %H:%M', time.strptime(tmp, '%Y-%m-%dT%H:%M:%S+05:30'))
                row[0] = tmp
                writer.writerow(row)
        i+=1
           