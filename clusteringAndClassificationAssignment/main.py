"""Main file for clustering and classification assignment.
"""

import matplotlib.pyplot as plt 
import clustering
import dataETL
from numpy import arange
import HCS 


if __name__ == '__main__':
    
    ### Import data 
    data_unselected, celllinenames_unselected, genes = dataETL.extractData("data/GDSC_RNA_expression.csv")
    data = dataETL.selectData(data_unselected)
    celllinenames = dataETL.selectData(celllinenames_unselected)
    
    ### Clustering 
    
    ## k-means and silhouette analysis
    
    
    ## Highly connected subgraph clustering
    corrCoef = clustering.overallCorrelationcoefficients(data, celllinenames)
    # print(len(corrCoef))
    # print(list(corrCoef.keys())[0])
    thresholds = arange(0, 1.01, 0.01)
    f = []
    for c in thresholds:
        f.append(clustering.nodepairFraction(corrCoef, c))
    
    # plot
    # plt.plot(thresholds, f)
    # plt.xlabel('c')
    # plt.ylabel('f(c)')
    # plt.grid()
    # plt.show()
    # f(c) ongeveer 0.1 voor c = 0.66
    
    edges = clustering.createEdges(0.66, corrCoef)
    # edgesTest = [('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'd'), ('c', 'd'), ('c', 'e'), ('d', 'e')]

    # graph1 = HCS.Graph(edges)
    
    nrIt = 50
    cuts = []
    maxIt = 5*nrIt
    while nrIt > 0 and maxIt > 0:
        graph = HCS.Graph(edges)
        nrCuts = graph.kargerMinCut()
        if nrCuts != 0:        
            cuts.append(nrCuts)
            nrIt -= 1
        maxIt -= 1

    minCuts = min(cuts)
    print(cuts)
    print(minCuts)
    
    
    
    
    
    
