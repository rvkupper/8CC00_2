"""Script for HCS clustering.
"""

import random

class Graph:
    def __init__(self, edges):
        graph = {}
        for edge in edges:
            node1 = edge[0]
            node2 = edge[1]
            if node1 not in graph:
                graph[node1] = []
            
            if node2 not in graph:
                graph[node2] = []
            graph[node1].append(node2)
            graph[node2].append(node1)
        
        self.graph = graph 
        self.nodes = list(self.graph.keys())
    
    def removeNode(self, node) -> None:
        # remove from self.nodes 
        self.nodes.remove(node)
        
        # remove from self.graph
        toRemove = self.graph.pop(node)
        for item in toRemove:
            self.graph[item].remove(node)
        
                
    def contractEdge(self, v, w) -> None:
        for node in self.graph[w]:
             if node != v:  
                 self.graph[v].append(node)
             self.graph[node].remove(w)  
             if node != v:
                  self.graph[node].append(v)
        del self.graph[w]  
        
        
    def kargerMinCut(self) -> int:
        while len(self.graph) > 2:
             node1 = random.choice(list(self.graph.keys()))
             if self.graph[node1] == []:
                 del self.graph[node1]
                 continue
             node2 = random.choice(self.graph[node1])
             self.contractEdge(node1, node2)
        mincut = len(self.graph[list(self.graph.keys())[0]])
        return mincut
        

        
