import networkx as nx
import matplotlib.pyplot as plt
import os

G = nx.Graph()
file=open("chain1008","r")
x=[]
for line in file:
	line = line.strip().split()
	print line[0], line[1]
	'''y=[]
	for number in line.split():
		y.append(number)'''
	y=tuple([int(line[0]), int(line[1])])
	x.append(y)

G.add_edges_from(x)
nx.draw_networkx(G)
#pos = nx.spring_layout(G)
#print(pos)
#nx.draw_networkx_nodes(G,pos, with_labels=True)
#nx.draw_networkx_labels(G, pos)
#nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
#nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrows=True)
plt.show()
nx.write_dot(G, 'test.dot')
nx.draw_graphviz(G, prog='dot')
plt.show()