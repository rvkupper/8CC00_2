"""Python scipt for clustering of data by means of k-means and ...
"""

def kMeans(data: set, k: int, distMethod: str) -> set:
    """k-means algorithm, using the distMethod to calculate 
    the distance between data points.
    
    :param k: integer to decide the number of centroids.
    :param distMethod: Method by which the disctance between data points needs to be chosen.
    :returns: a set of all datapoints, subdivided in their clusters.
    """
    
    
def squaredEuclideanDist(u, v) -> float:
    """Calculate the Euclidean squared distance between u and v.
    
    """
    assert type(u) == type(v), "Types of u and v must be the same."
    
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
        
u = 2.
v = 1.5
print(squaredEuclideanDist(u, v))
