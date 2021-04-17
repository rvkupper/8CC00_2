import dataETL
import classification
import clustering
from Graph import Graph
import copy

# data = [2, 6, 2, 7, 1, 4, 3, 0]
# 
# print(classification.nearestNeighbour(data, 5, 4))


edges = [('a', 'c'), ('a', 'b'), ('a', 'e'), ('b', 'c'), ('b', 'd'), 
('c', 'd'), ('c', 'e'), ('d', 'e'), ('d', 'f'), ('e', 'g'), ('f', 'g'), 
('f', 'h'), ('f', 'i'), ('g', 'j'), ('g', 'k'), ('g', 'l'), ('h', 'i'), 
('i', 'j'), ('j', 'k'), ('j', 'l'), ('k', 'l')]

myGraph = Graph(edges)
# print(myGraph.graph)
# 
# nrIt = 10
# cuts = []
# gs = []
# maxIt = 5*nrIt
# while nrIt > 0 and maxIt > 0:
#     nrCuts , g = clustering.kargerMinCut(copy.deepcopy(myGraph.graph))
#     if nrCuts != 0:
#         cuts.append(nrCuts)
#         gs.append(g)
#         nrIt -= 1
#     maxIt -= 1
# 
# minCuts = min(cuts)
# kargergraph = gs[cuts.index(minCuts)]
# print(minCuts)
# print(kargergraph)
# 
# h1, h2 = clustering.karger2subgraph(kargergraph, edges)
# print(h1)
# print(h2)

clusters = clustering.HCS(copy.deepcopy(myGraph.graph), edges, nrIt = 50)

nrNodes = 0
for cluster in clusters:
    print(list(cluster.keys()))
    nrNodes += len(list(cluster.keys()))
print(nrNodes)
