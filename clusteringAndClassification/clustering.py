"""Python scipt for clustering of data by means of k-means, evaluation with silhouette scores and HCS clustering.
"""

import random
import dataProcessing
from collections.abc import Iterable
from Graph import Graph
import copy

def squaredEuclideanDist(u, v) -> float:
    """Calculate the Euclidean squared distance between u and v.
    
    :param u: 1D or ND coordinate in int or float, or list or tuple respecitvely.
    :param v: 1D or ND coordinate in int or float, or list or tuple respecitvely.
    :returns: float of Euclidean squared distance between u and v.
    """
    if isinstance(u, float) or isinstance(u, int):
        # 1D case
        u = [u]
        v = [v]
        D = 0
    elif isinstance(u, list) or isinstance(u, tuple):
        # Multiple D case
        assert len(u) == len(v), "Length of u and v must be the same." 
        D = len(u) - 1
    else:
        raise TypeError 
        print("Type of u and v must be int, float, list or tuple.")
    
    dist = 0
    while D >= 0:
        dist1D = (u[D] - v[D])**2
        dist += dist1D
        D -= 1
                
    return dist
    
def calculateCentroids(clusteredData: list, dim: int) -> list:
    """Recalculate the new centroid based on the averages in the old cluster configuration.
    
    :param clusteredData: list containing the old clusters.
    :param dim: required dimensions for the centroids.
    :returns: List containing new centroids on the position of the average of the cluster.
    """
    new_centroids = []
    # Check dimensions
    if dim == 1:
        # 1D case
        for cluster in clusteredData:
            cluster_avg = sum(cluster)/len(cluster)
            centroid = cluster_avg
            new_centroids.append(centroid)
    else:
        # Multiple D case
        for cluster in clusteredData:
            N = len(cluster)
            if N == 0: # Avoid division by 0
                N = 1
            centroid = tuple(sum(x[i] for x in cluster)/N for i in range(dim))
            new_centroids.append(centroid)
    
    return new_centroids


def kMeans(data: list, k: int, distMethod: str, maxit: int) -> list:
    """
    k-means algorithm, using the distMethod to calculate the distance between data points.
    
    :param data: list of int, float, list or tuple values for datapoints.
    :param k: integer to decide the number of centroids.
    :param distMethod: Method by which the distance between data points needs to be chosen.
    :param maxit: Maximum number of iterations
    :returns: a list of sets per cluster.
    """
    # Generate random start centroids  
    centroids = []
    
    if isinstance(data[0], float) or isinstance(data[0], int):
        # 1D case
        dim = 1
        min_data = min(data)
        max_data = max(data)
        for i in range(k):
            centroids.append(random.uniform(min_data, max_data))
        
    elif isinstance(data[0], list) or isinstance(data[0], tuple):
        # Multiple D case
        dim = len(data[0])
        min_data = min(min(data))
        max_data = max(max(data))   
        for i in range(k):
            coord = ()
            for j in range(dim):
                coord = coord + (random.uniform(min_data, max_data),)
            centroids.append(coord)
            
    looping = True
    itnr = 0
    old_clusters = []
    
    while looping == True and itnr <= maxit:
        
        # Generate list of empty clusters
        clusters = []
        for i in range(k):
            clusters.append(set())
        
                
        # Fill clusters
        for datapoint in data:
            
            dist = float('inf')
            i = 0
            index = 0
            while i < len(centroids):
                d = squaredEuclideanDist(datapoint, centroids[i])
                if d < dist:
                    dist = d 
                    index = i
                i += 1
            clusters[index].add(tuple(datapoint))
            
        # Calculate new centroids
        new_centroids = calculateCentroids(clusters, dim)
        
        itnr += 1
        
        if new_centroids == centroids or clusters == old_clusters:
            # Stop condition
            # print('centroid stop', new_centroids == centroids)
            # print('cluster stop', clusters == old_clusters)
            looping = False
             
        else:
            # Continue iterating and update parameters
            # print('Iteration', itnr)
            centroids = new_centroids
            old_clusters = clusters
        
    
    return clusters
    
        
def silhouetteScore(clusteredData: list) -> tuple:
    """Calculate silhouette score for clustered data. \
    Function returns tuple containing on the first index \
    the silhouette score for the clustering and in the \
    second index a dict containing the silhouettes for all \
    datapoints.
    
    :param clusteredData: list containing sets of data per cluster 
    :returns: (float, dict) where the float is the overall silhouette score for the clustering and the dict contains the silhouette per datapoint like {(coordinate): silhouette}
    :examples:
    
    >>> v = [{(1.5, 0.5), (1., 1.5), (0.5, 0.5), (0.5, 2.)}, {(6, 6), (5.5, 6), (6, 5.5)}, {(4.5, 2.), (4., 2.), (3.5, 1.5)}]
    >>> x, y = silhouetteScore(v)
    0.9352832294102621 {(1.0, 1.5): 0.8928571428571429, (0.5, 0.5): 0.924812030075188, (1.5, 0.5): 0.8567493112947658, (0.5, 2.0): 0.8986666666666667, (6, 6): 0.9884169884169884, (6, 5.5): 0.9858490566037735, (5.5, 6): 0.9873949579831933, (4.5, 2.0): 0.9482758620689655, (3.5, 1.5): 0.9147540983606557, (4.0, 2.0): 0.9550561797752809}
    """
    meanWithinClusters = {}
    meanOtherClusters = {}
    silhouettes = {}
    for cluster in clusteredData:
        # if len(cluster) == 0:
        #     print("Empty cluster present")
        datapoints = list(cluster)
        
        # Create list for the clusters that active_point is not part of
        otherClusters = clusteredData.copy()
        otherClusters.remove(cluster)
        
        distInCluster = []
        for active_point in datapoints:
            
            # Mean distance within it's own cluster 
            for point in datapoints:
                d = squaredEuclideanDist(active_point, point)
                distInCluster.append(d)
            if len(distInCluster) != 1: # Avoid division by 0
                meanDist = sum(distInCluster)/(len(distInCluster) - 1)
            else:
                meanDist = sum(distInCluster)
            meanWithinClusters[active_point] = meanDist
            
            # Mean distance to all points from the nearest cluster 
            for otherCluster in otherClusters:
                distOtherCluster = []
                
                for otherPoint in list(otherCluster):
                    s = squaredEuclideanDist(active_point, otherPoint)
                    distOtherCluster.append(s)
                
                if len(distOtherCluster) != 0: # Avoid division by 0
                    meanOtherDist = sum(distOtherCluster)/len(distOtherCluster)
                else:
                    meanOtherDist = sum(distOtherCluster)
                                
                if active_point in meanOtherClusters:
                    if meanOtherClusters[active_point] > meanOtherDist:
                        meanOtherClusters[active_point] = meanOtherDist                                                
                else:
                    meanOtherClusters[active_point] = meanOtherDist
            
            # Calculate silhouette for each datapoint        
            a = meanDist 
            b = meanOtherClusters[active_point]
            
            if not (a == 0 and b == 0):
                silhouette = (b - a) / max(a, b)
            else:
                silhouette = 0
            silhouettes[active_point] = silhouette
    
    # Calculate overall silhouette score
    silhouetteScore = sum(silhouettes.values())/len(silhouettes)                
    return silhouetteScore, silhouettes 
            

def overallCorrelationcoefficients(data: Iterable, names: list) -> dict:
    """Create a dict in which for each node pair the correlation coefficient is calculated.
    
    :param data: iterable containing coordinates for each datapoint.
    :param names: isterable containing respective names for each datapoint in data.
    :returns: Dict like {(node1, node2): correlationcoefficient} where the nodes are strings and the correlation coefficient is a float.
    """
    correlations = {}
    data2 = data.copy()
    names2 = names.copy()
    for i, datapoint in enumerate(data):
        name1 = names[i]
        data2.remove(datapoint)
        names2.remove(name1)
        for j, secondDatapoint in enumerate(data2):
            name2 = names2[j]
            pair = (name1[0], name2[0])
            coef = dataProcessing.correlationCoefficient(datapoint, secondDatapoint)
            correlations[pair] = coef
    return correlations
            
    

def nodepairFraction(overallCorrelations: dict, c:float) -> float:
    """Calculate the fraction of node pairs that have an absolute value of their correlation coefficient of at least c.
    
    :param overallCorrelations: dictionary containing node pairs and their correlations (can be calculated with the function overallCorrelationcoefficients)
    :param c: Threshold for fraction.
    :returns: fraction of number of node pairs that is above threshold.
    """
    nodepairs = overallCorrelations.keys()
    coefs = overallCorrelations.values()
    
    nrOfPairs = 0
    for coef in coefs:
        if abs(coef) >= c:
            nrOfPairs += 1
    
    frac = nrOfPairs/len(nodepairs)
    
    return frac
    
def createEdges(c: float, edgesdict: dict) -> list:
    """Evaluate whether the correlation of an edge is above c and return \
    a list of edges that does.
    
    :param c: threshold value for correlation coefficient of edge 
    :param edgesdict: dictionary containing all possible edges and their correlation coefficients.
    :returns: List like [(node1, node2), (node1, node3)] where nodes are strings.
    """
    edges = []
    for key, val in edgesdict.items():
        if val >= c:
            edges.append(key)
    
    return edges
    
def contractEdge(graph: dict, v: str, w:str) -> None:
    """Edgecontraction. Create one supernode from two nodes.
    
    Warning: The original graph is overwritten.
    
    :param graph: dict of graph in which edges need to be contracted.
    :param v: first node to be merged into supernode.
    :param w: second node to be merged into supernode.
    """
    # print(v, graph[v])
    # print(w, graph[w])
    if isinstance(v, str):
        if isinstance(w, str):
            supernode = (v, w)
        else:
            supernode = (v, ) + w 
    elif isinstance(w, str):
        supernode = v + (w, )
    else:
        supernode = v + w
    
    graph[supernode] = graph[v]
    for node in graph[w]:
         if node != v:  
             graph[supernode].append(node)
         # if w in graph[node]:
         graph[node].remove(w)  
         if node != v:
              graph[node].append(supernode)
    for node in graph[v]:
         if v in graph[node]:
             graph[node].remove(v)
             graph[node].append(supernode)
    del graph[w]  
    del graph[v]
    
    
def kargerMinCut(g: dict) -> tuple:
    """Perform a kargercut in a graph.
    
    :param g: dict of graph in which karger cut needs to be done.
    :returns: minimum nr of edges that need to be cut, graph that remains
    """
    while len(g) > 2:
         node1 = random.choice(list(g.keys()))
         # print('node1', node1)
         if g[node1] == []:
             del g[node1]
             # print('deleted')
             continue
         node2 = random.choice(g[node1])
         # print('node2', node2)
         contractEdge(g, node1, node2)
    
    mincut = len(g[list(g.keys())[0]])
    return mincut, g
    
def highlyConnected(graph: dict, mincut:int) -> bool:
    """Decide whether graph is highly connected.
    
    :param graph: dict of graph to decide on.
    :param mincut: minimum number of cuts.
    :returns: minimumcut > nrNodes/2
    """
    nrNodes = len(graph)
    return mincut > nrNodes/2

def karger2subgraph(supernodesgraph: dict, originalEdges: list) -> tuple:
    """Create subgraphs from the resulting supernodes graph after kargercut.
    
    :param supernodesgraph: the two supernodes that remain after Karger cut.
    :param originalEdges: list of edges from the original graph (before the cut).
    :returns: tuple containing two subgraphs in dict format.
    """
    subgraphs = list(supernodesgraph.keys())
    graphs = []
    
    for subgraph in subgraphs:
        subgraphEdges = []
        for edge in originalEdges:
            node1 = edge[0]
            node2 = edge[1]
            if node1 in subgraph and node2 in subgraph:
                subgraphEdges.append(edge)
        graphs.append(Graph(subgraphEdges).graph)
    return graphs[0], graphs[1]
    
def HCS(graph: dict, originalEdges: list, nrIt:int = 10, clusters = []) -> list:
    """Highly connected subgraph clustering, using Karger cut.
    
    :param graph: graph dict on which to perform HCS clustering.
    :param originalEdges: edges of the graph.
    :param nrIt: nr of iterations that the kargercut should be performed to assume the minimum cut is reached.
    :param clusters: parameter to remember previous clusters during recursion. Should be the empty list when called for the first time.
    :returns: list containing the clusters in graph dict format. 
    """
    # Check disconnected subgraphs
    if len(graph) == 0:
        # print("Singlet thrown away")
        return
    
    # Determine mincut with karger
    cuts = []
    gs = []
    newIt = 0
    maxIt = 5*nrIt
    while nrIt > 0 and maxIt > 0:
        nrCuts , g = kargerMinCut(copy.deepcopy(graph))
        if nrCuts != 0:
            cuts.append(nrCuts)
            gs.append(g)
            nrIt -= 1
            newIt +=1
        maxIt -= 1

    minCuts = min(cuts)
    
    # Check if highly connected 
    if highlyConnected(graph, minCuts):
        clusters.append(graph)
        
    else:
        kargergraph = gs[cuts.index(minCuts)]
        h1, h2 = karger2subgraph(kargergraph, originalEdges)
        HCS(h1, originalEdges, nrIt = newIt, clusters = clusters)
        HCS(h2, originalEdges, nrIt = newIt, clusters = clusters)
    
    return clusters

    
