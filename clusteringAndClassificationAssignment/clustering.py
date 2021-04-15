"""Python scipt for clustering of data by means of k-means and evaluation with silhouette scores.
"""

import random

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
            clusters[index].add(datapoint)
            
        # Calculate new centroids
        new_centroids = calculateCentroids(clusters, dim)
        
        itnr += 1
        
        if new_centroids == centroids or clusters == old_clusters:
            # Stop condition
            print('centroid stop', new_centroids == centroids)
            print('cluster stop', clusters == old_clusters)
            looping = False
             
        else:
            # Continue iterating and update parameters
            print('Iteration', itnr)
            centroids = new_centroids
            old_clusters = clusters
        
    
    return clusters
    
        
def silhouetteScore(clusteredData: list) -> tuple:
    """Calculate silhouette score for clustered data. Function returns tuple containing on the first index the silhouette score for the clustering and in the second index a dict containing the silhouettes for all datapoints.
    
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
            meanDist = sum(distInCluster)/(len(distInCluster) - 1)
            meanWithinClusters[active_point] = meanDist
            
            # Mean distance to all points from the nearest cluster 
            for otherCluster in otherClusters:
                distOtherCluster = []
                
                for otherPoint in list(otherCluster):
                    s = squaredEuclideanDist(active_point, otherPoint)
                    distOtherCluster.append(s)
                
                meanOtherDist = sum(distOtherCluster)/len(distOtherCluster)
                                
                if active_point in meanOtherClusters:
                    if meanOtherClusters[active_point] > meanOtherDist:
                        meanOtherClusters[active_point] = meanOtherDist                                                
                else:
                    meanOtherClusters[active_point] = meanOtherDist
            
            # Calculate silhouette for each datapoint        
            a = meanDist 
            b = meanOtherClusters[active_point]
            
            silhouette = (b - a) / max(a, b)
            silhouettes[active_point] = silhouette
    
    # Calculate overall silhouette score
    silhouetteScore = sum(silhouettes.values())/len(silhouettes)                
    return silhouetteScore, silhouettes 
            
    
    
    
    
    
    
    
l = [(1.2, 1.5), (0.6, 0.5), (0.5, 1.7), (1.5, 0.5), (6, 6), (5.7, 6), (6, 5.4)]
# print(kMeans(l, 2, 'a', 10))
v = [{(1.5, 0.5), (1., 1.5), (0.5, 0.5), (0.5, 2.)}, {(6, 6), (5.5, 6), (6, 5.5)}, {(4.5, 2.), (4., 2.), (3.5, 1.5)}]
x, y = silhouetteScore(v)
print(x, y)
