import matplotlib.pyplot as plt
import csv
import time

x = []
y = []

with open('aeroqual_co2.csv','r') as csvfile:
	plots = csv.reader(csvfile, delimiter = ',')
	i=1
	for row in plots:
		 #convert timestamp of format 08 Sep 2022 19:22 to datetime object
		if i==1:
			i=0
			continue
		if (row[3]!='') & ((float(row[3]))<=2000) :
			x.append(time.mktime(time.strptime(row[0], "%d %b %Y %H:%M")))
			y.append(float(row[3]))

plt.plot(x, y, color = 'g', label = "Ideal")
print(x[0])
a=[]
b=[]

with open('feeds.csv', 'r') as f:
	plots = csv.reader(f, delimiter = ',')
	i=1
	for row in plots:
		# print(row)
		if i==1:
			i=0
			continue
		# print(len(row))
		if len(row)>0:
			# print(row[2])
			i+=2
			if (row[2]!='')  :
				# print("yes")
				if  (((float(row[2]))<=2000) & (i%5==0)):
					print(row[2])
					a.append(time.mktime(time.strptime(row[0], '%Y-%m-%dT%H:%M:%S%z')))
					b.append(float(row[2]))

plt.plot(a, b, color = 'r', label = "Co2")
print(b)
print(a)
plt.xlabel('Time')
plt.ylabel('Values')
plt.title('CO2')

# # print(y)
# print(b)

plt.legend()
plt.show()
