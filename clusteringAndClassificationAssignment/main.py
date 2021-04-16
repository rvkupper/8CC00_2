"""Main file for clustering and classification assignment.
"""

import matplotlib.pyplot as plt 
import clustering
import classification
import dataETL
from numpy import arange
import HCS 
from collections import Counter


if __name__ == '__main__':
    
    ### Import data 
    data_unselected, celllinenames_unselected, genes = dataETL.extractData("data/GDSC_RNA_expression.csv")
    data = dataETL.selectData(data_unselected)
    celllinenames = dataETL.selectData(celllinenames_unselected)
    labels = dataETL.extractLabels('data/GDSC_metadata.csv')

    ### Clustering 
    
    ## k-means and silhouette analysis
    
    print("k silhouette score")
    scores = []
    for k in range(2, 9):
        scorePerK = []
        for i in range (20):
            clusters = clustering.kMeans(data, k, 'sqeu', 1000)
            totalSilhouette, silhouettes = clustering.silhouetteScore(clusters)
            scorePerK.append(totalSilhouette)
        score = max(scorePerK)
        scores.append(max(scorePerK))
        print(k, score)
    
    
    
    
    ## Highly connected subgraph clustering
    
    corrCoef = clustering.overallCorrelationcoefficients(data, celllinenames)
    thresholds = arange(0, 1.01, 0.01)
    f = []
    for c in thresholds:
        f.append(clustering.nodepairFraction(corrCoef, c))
    
    # plot
    plt.plot(thresholds, f)
    plt.xlabel('c')
    plt.ylabel('f(c)')
    plt.grid()
    plt.show() # f(c) ongeveer 0.1 voor c = 0.66
    
    edges = clustering.createEdges(0.66, corrCoef)
    
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
    
    
    ### Classification 
    errorScore = Counter()
    
    for i in range(len(data)):
        
        # Generate training dataset and point of interest 
        trainingset, trainingnames, point_of_interest = classification.generateTrainingset(data, i, celllinenames)
        datapoint = point_of_interest[1]
        datapointname = point_of_interest[0][0]
        
        # Perfrom k-nearest neighbours
        for k in range(1, 10):
            found_label = classification.nearestNeighbour(trainingset, datapoint, k, trainingnames, labels)

                    
            # Check found label with actual label 
            if not classification.checkLabel(datapointname, found_label, labels):
                title = "k = "+str(k)
                errorScore[title] += 1
            
            
    print(errorScore)        
            
    
