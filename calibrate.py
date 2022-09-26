import matplotlib.pyplot as plt
import time
from collections import defaultdict
import csv
import numpy as np

co2 = defaultdict(list)
pm = defaultdict(list)

targetco2 = defaultdict(list)
targetpm = defaultdict(list)

with open('newv.csv' , 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    i=0
    for row in reader:
        if len(row)>0:
            if row[1]!='' and row[2]!='' and row[4]!='':
                co2[row[0]].append(float(row[2]))
                pm[row[0]].append(float(row[4]))
    

co2f = defaultdict(list)
pmf = defaultdict(list)

for key in co2:
    co2f[key] = sum(co2[key])/len(co2[key])
    pmf[key] = sum(pm[key])/len(pm[key])

with open('aeroqual_PM.csv' , 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    i=0
    for row in reader:
        if i!=0 and row[1]!='' and row[2]!='':
            # targetco2[row[0]].append(float(row[3])).
            targetpm[row[0]].append(float(row[4])*1000)
        i+=1

# perform linear regression between co2f and targetco2
# perform linear regression between pmf and targetpm
keys = pmf.keys() & targetpm.keys()

x=[]
y=[]

maxi = 0
maxj = 0
maxk = 0

for key in keys:
    if pmf[key]<500 and abs(targetpm[key][0]-pmf[key]) <100:
        x.append(pmf[key])
        y.append(targetpm[key][0])
        
    print( key , pmf[key],targetpm[key][0])
    

print(maxi)
print(maxj)
print(maxk)

nx = np.array(x)
ny  = np.array(y)

# print(nx)
# print(ny)

n = np.size(nx)
m_x, m_y = np.mean(nx), np.mean(ny)
SS_xy = np.sum(ny*nx) - n*m_y*m_x
SS_xx = np.sum(nx*nx) - n*m_x*m_x
b_1 = SS_xy / SS_xx
b_0 = m_y - b_1*m_x
print(b_0, b_1)

def plot_regression_line(x, y, b):
    # plotting the actual points as scatter plot
    plt.scatter(x, y, color = "m",
               marker = "o", s = 30)
  
    # predicted response vector
    y_pred = b[0] + b[1]*x
  
    # plotting the regression line
    plt.plot(x, y_pred, color = "g")
  
    # putting labels
    plt.xlabel('x')
    plt.ylabel('y')
  
    # function to show plot
    plt.show()
  
plot_regression_line(nx, ny, [b_0, b_1])

# # do linear regression and find relation between x and y
# n = np.size(nx)
  
# # mean of x and y vector
# m_x = np.mean(nx)
# m_y = np.mean(ny)

# # calculating cross-deviation and deviation about x
# SS_xy = np.sum(ny*nx) - n*m_y*m_x
# SS_xx = np.sum(nx*nx) - n*m_x*m_x

# # calculating regression coefficients
# b_1 = SS_xy / SS_xx
# b_0 = m_y - b_1*m_x

# # our linear reg is y = b_0 + b_1*x
# print(b_0, b_1)
    
