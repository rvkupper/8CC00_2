"""Python scipt for clustering of data by means of k-means and ...
"""

import random

def squaredEuclideanDist(u, v) -> float:
    """Calculate the Euclidean squared distance between u and v.
    
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



def kMeans(data: list, k: int, distMethod: str) -> set:
    """
    k-means algorithm, using the distMethod to calculate 
    the distance between data points.
    
    :param k: integer to decide the number of centroids.
    :param distMethod: Method by which the disctance between data points needs to be chosen.
    :returns: a list of sets per cluster.
    """
    # Generate random start centroids  
    centroids = []
    
    if isinstance(data[0], float) or isinstance(data[0], int):
        # 1D case
        min_data = min(data)
        max_data = max(data)
        for i in range(k):
            centroids.append(random.uniform(min_data, max_data))
        
    elif isinstance(data[0], list) or isinstance(data[0], tuple):
        # Multiple D case
        min_data = min(min(data))
        max_data = max(max(data))   
        for i in range(k):
            coord = ()
            for j in range(len(data[0])):
                coord = coord + (random.uniform(min_data, max_data),)
            centroids.append(coord)
            
    
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
    return clusters     
        
    

        
