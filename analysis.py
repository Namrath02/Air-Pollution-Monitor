import matplotlib.pyplot as plt
import time
from collections import defaultdict
import csv
import numpy as np


co2 = []
time = []

with open('newv.csv' , 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    i=0
    for row in reader:
        if len(row)>0:
            if row[1]!='' and row[2]!='' and row[4]!='':
                # extract day of the week from format 08 Sep 2022 19:27
                conv = time.strptime(row[0], '%d %b %Y %H:%M').tm_wday
                if conv == 2:
                    co2.append(float(row[4]))
                    # extract time in hours and minutes from the format 08 Sep 2022 19:27
                    time.append( time.strptime(row[0], '%d %b %Y %H:%M').tm_hour + time.strptime(row[0], '%d %b %Y %H:%M').tm_min/60 )
                    # tim
        
plt.plot(time, co2)
plt.xlabel('Time')
plt.ylabel('CO2')
plt.show()



                
    