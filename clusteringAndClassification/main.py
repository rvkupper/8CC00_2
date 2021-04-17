"""Main file for clustering and classification assignment.
"""

import matplotlib.pyplot as plt 
import clustering
import classification
import dataETL
from numpy import arange
from Graph import Graph
from collections import Counter
import copy


if __name__ == '__main__':
    
    ### Import data 
    data_unselected, celllinenames_unselected, genes = dataETL.extractData("data/GDSC_RNA_expression.csv")
    data = dataETL.selectData(data_unselected)
    celllinenames = dataETL.selectData(celllinenames_unselected)
    labels = dataETL.extractLabels('data/GDSC_metadata.csv')

    ### ------------------------------------------------------------------------
    ### Clustering 
    
    ## k-means and silhouette analysis
    print("k-means clustering")
    
    print("k | silhouette score")
    scores = []
    for k in range(2, 9):
        scorePerK = []
        for i in range (20):
            clusters = clustering.kMeans(data, k, 'sqeu', 1000)
            totalSilhouette, silhouettes = clustering.silhouetteScore(clusters)
            scorePerK.append(totalSilhouette)
        score = max(scorePerK)
        scores.append(max(scorePerK))
        print(k, "|", score)
    
    
    ## Highly connected subgraph clustering
    
    corrCoef = clustering.overallCorrelationcoefficients(data, celllinenames)
    
    # Calculate f(c) for different c
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
    
    myGraph = Graph(edges)
    
    clustergraphs = clustering.HCS(copy.deepcopy(myGraph.graph), edges, nrIt = 50)
    
    nrNodes = 0
    clusternodes = []
    for cluster in clustergraphs:
        print("HCS cluster:", list(cluster.keys()))
        clusternodes.append(list(cluster.keys()))
        nrNodes += len(list(cluster.keys()))
    
    
    
    ###-------------------------------------------------------------------------
    ### Classification 
    
    ## k nearest neighbours classification
    
    errorScore_kNearest = Counter()
    
    for i in range(len(data)):
    
        # Generate training dataset and point of interest 
        trainingset, trainingnames, point_of_interest = classification.generateTrainingset(data, i, celllinenames)
        datapoint = point_of_interest[1]
        datapointname = point_of_interest[0][0]
    
        # Perfrom k-nearest neighbours
        for k in range(1, 26):
            found_label = classification.nearestNeighbour(trainingset, datapoint, k, trainingnames, labels)
    
            # Check found label with actual label 
            if not classification.checkLabel(datapointname, found_label, labels):
                title = "k = "+str(k)
                errorScore_kNearest[title] += 1
    
    print("Error score k-nearest neighbours per k:", errorScore_kNearest)
    
    
    ## HCS classification errorscore 
    errorScoreHCS = 0
    
    for cluster in clusternodes:
        # Determine clusterlabel
        labelcount = Counter()
        for node in cluster:
            nodelabel = labels[node]
            labelcount[nodelabel] += 1
        clusterlabel = labelcount.most_common(1)[0][0]
    
        for node in cluster:
            # Count number of wrongly labelled nodes
            if not classification.checkLabel(node, clusterlabel, labels):
                errorScoreHCS += 1    
    
    
    print("Error score for HCS classification:", errorScoreHCS)
    
    
