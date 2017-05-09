import networkx as nx
import matplotlib.pyplot as plt
import numpy
import numpy as np
import pylab

def refreshGraph():
    plt.clf()
    nx.draw_networkx_nodes(T, pos, nodelist=black, node_color='k', node_size=400, alpha=0.8)
    nx.draw_networkx_nodes(T, pos, nodelist=white, node_color='w', node_size=400, alpha=0.8)
    nx.draw_networkx_edges(T,pos,width=1.0, alpha=0.5)
    plt.axis('off')
    plt.axis((-4,4,-1,3))
    fig.patch.set_facecolor('white')
    plt.show()

def onClick(event):
    (x,y)   = (event.xdata, event.ydata)

    for i in allNodes:
        node = pos[i]
        distance = pow(x-node[0],2)+pow(y-node[1],2)
        if distance < 0.1:
            T.remove_node(i)
            if i in black: black.remove(i)
            if i in white: white.remove(i)
            allNodes.remove(i)
            refreshGraph()

fig, ax = plt.subplots()
fig.canvas.mpl_connect('button_press_event', onClick)

T = nx.Graph()

### Nodes
white, black = [1, 4, 5, 6, 7], [2, 3]
allNodes = white+black

for node in allNodes:      T.add_node(node)

### Edges
T.add_edge(1, 2)
T.add_edge(1, 3)
T.add_edge(2, 4)
T.add_edge(2, 5)
T.add_edge(3, 6)
T.add_edge(3, 7)

### Positions of the nodes
pos={}
pos[1]=numpy.array([ 0,0])
pos[2]=numpy.array([-2,1])
pos[3]=numpy.array([ 2,1])
pos[4]=numpy.array([-3,2])
pos[5]=numpy.array([-1,2])
pos[6]=numpy.array([ 1,2])
pos[7]=numpy.array([ 3,2])

### Draw nodes and edges
refreshGraph()