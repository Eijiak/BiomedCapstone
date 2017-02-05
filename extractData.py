# Note Ctrl+C is Keyboard interrupt

import urllib.request
import re
import matplotlib.pyplot as plt
import numpy
from datetime import datetime

# Initialize variables
values=[]
plt.plot(values)

while(1):
    with urllib.request.urlopen('http://192.168.4.1/read') as f: # Reads analog data from ESP
        y=f.read(10)
        convData = y.decode("utf-8") # Convert from byte
        values.append(convData)
        if len(values)>30:
            del values[:1]
            plt.clf()
            
        # Plot values
        plt.plot(values)
        plt.draw()
        plt.pause(0.001)
        print(str(datetime.now()))
