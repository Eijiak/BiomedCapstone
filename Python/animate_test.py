import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    graph_data = open('example.txt', 'r').read()
    print('hi')
    lines = graph_data.split('\n')
    xs = []
    ys = []
    print(graph_data)
    for line in lines:
        if len(line) > 1:
            x,y = line.split(',')
            xs.append(x)
            ys.append(y)
    ax1.clear()
    ax1.plot(xs,ys)


ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
