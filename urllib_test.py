import urllib.request
import re
import matplotlib.pyplot as plt
import numpy

hl, = plt.plot([], [])

def update_line(hl, new_data):
    hl.set_xdata(numpy.append(hl.get_xdata(), new_data))
    hl.set_ydata(numpy.append(hl.get_ydata(), new_data))
    plt.draw()

s = 'b\'78\''
'''
with urllib.request.urlopen('http://192.168.4.1/read') as f:
	y=f.read(10)
	print(y.decode("utf-8"))
'''
#print(re.search(r'\'(.*)\'', f.read(10)).group(1))
#s2=int(re.search(r'\'(.*)\'', s).group(1))
#s3=str(s2)
#print(s3)
values=[]
plt.plot(values)
#plt.show()
#plt.pause(0.05)
#plt.ion()
while(1):
    with urllib.request.urlopen('http://192.168.4.1/read') as f:
        y=f.read(10)
        print(y)
        convData = y.decode("utf-8")
        print(convData)
        values.append(convData)
        if len(values)>30:
            del values[:1]
            plt.clf()
        plt.plot(values)
        plt.draw()
        plt.pause(0.001)



'''
print("Raw:", f.read(10))
y = f.read(10)
convData = y.decode("utf-8")
print(convData)
#update_line(hl, int(re.search(r'\'(.*)\'', f.read(10)).group(1)))
#print(int(re.search(r'\'(.*)\'', f.read(10)).group(1))) 
'''
