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
        """Remove node from Graph.
        """
        # remove from self.nodes 
        self.nodes.remove(node)
        
        # remove from self.graph
        toRemove = self.graph.pop(node)
        for item in toRemove:
            self.graph[item].remove(node)
        
                
    def removeEdge(self, node1, node2) -> None:
        """Remove edge between node 1 and node 2 from Graph.
        """
        # Remove from self.graph 
        self.graph[node1].remove(node2)
        self.graph[node2].remove(node1)
        

        
