# Note Ctrl+C is Keyboard interrupt

import urllib.request
import matplotlib.pyplot as plt
import numpy
from datetime import datetime

# Initialize variables
values=[]
n = 3
plt.plot(values)


while(1):
	
    with urllib.request.urlopen('http://192.168.4.1/') as f: # Reads analog data from ESP
        y=f.read(2000)
        convData = y.decode("utf-8") # Convert from byte
        values = values + [convData[i:i+n] for i in range(0, len(convData),n)]
     #   print(values);
        """
        if len(values)>30:
            del values[:1]
            plt.clf()
	"""
    # Plot values
    plt.plot(values)
    plt.draw()
    plt.pause(0.001)
#    print(str(datetime.now()))
