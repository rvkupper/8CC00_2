"""Main file for clustering and classification assignment.
"""

import matplotlib.pyplot as plt 
import clustering
import dataETL
from numpy import arange


if __name__ == '__main__':
    
    ### Import data 
    data_unselected, celllinenames_unselected, genes = dataETL.extractData("data/GDSC_RNA_expression.csv")
    data = dataETL.selectData(data_unselected)
    celllinenames = dataETL.selectData(celllinenames_unselected)
    
    
    ### Clustering 
    
    ## k-means and silhouette analysis
    
    
    ## Highly connected subgraph clustering
    corrCoef = clustering.overallCorrelationcoefficients(data)
    thresholds = arange(0, 1.01, 0.01)
    f = []
    for c in thresholds:
        f.append(clustering.nodepairFraction(corrCoef, c))
    
    # plot
    plt.plot(thresholds, f)
    plt.xlabel('c')
    plt.ylabel('f(c)')
    plt.grid()
    plt.show()
    
    
    
    
    
