"""Script for k nearest neighbour classification and trainingsset generation.
"""

import clustering 
from collections.abc import Iterable
from collections import Counter
    
    
def findName(point: list, data: list, names: list) -> str:
    """Find name that belongs to a datapoint. Note that data and names indices should match.
    
    :param point: list containing coordinate of the point to be named.
    :param data: list containing all points, including above point.
    :param names: list containing respective names of points in data.
    :returns: name of point
    """
    assert len(data) == len(names), "data and names do not match"
    i = data.index(point)
    return names[i][0]
    
    
def nearestNeighbour(trainingset: Iterable, newDataPoint, k: int, trainingnames: list, labelsdict: dict, distMethod: str = "sqEucl") -> str:
    """Nearest neighbour algorithm for classification of data.
    
    :param trainingset: dataset that does not contain newDataPoint.
    :param newDataPoint: datapoint to be labelled. May be int, float, list or tuple.
    :param k: nr of neighbours to be considered.
    :param labelsdict: dict containing labels for datapoints in trainingset 
    :param distMethod: method of distance calculation to be used. (to be implemented)
    :returns: label for new datapoint
    """
    
    # Find k nearest neighbours
    # Calculate all distances
    distancesToNew = []
    for point in trainingset:
        dist = clustering.squaredEuclideanDist(point, newDataPoint)
        distancesToNew.append((dist, point))
    
    
    neighbours = []
    for i in range(k):
        nearest = min(distancesToNew)
        neighbour = nearest[1]
        neighbours.append(neighbour)
        distancesToNew.remove(nearest)
    
    foundLabels = Counter()
    for point in neighbours:
        name = findName(point, trainingset, trainingnames)
        label = labelsdict[name]
        foundLabels[label] += 1
    
    
    newLabel = foundLabels.most_common(1)[0][0]
    
    return newLabel
    
    
def checkLabel(datapointname: str, label: str, labelsdict: dict) -> bool:
    """Checks if assigned label to datapoint is correct according to the information in the labelsdict.
    
    :param datapointname: The node to be checked.
    :param label: The label to be checked
    :param labelsdict: The dict in which all labels for all datapoints are stored
    :returns: True if label is correct, False if incorrect.
    """
    return labelsdict[datapointname] == label 


def generateTrainingset(fulldataset: Iterable, i: int, names: list) -> tuple:
    """Generate a leave-one-out trainingsset at index i and return both.
    
    :param fulldataset: the full dataset to be used 
    :param i: the index of the point to be left out 
    :param names: list of names for the datapoints
    :returns: tuple containing trainingset, trainingnames, (new point name, new point coordinate)
    """
    dataset = fulldataset.copy()
    names2 = names.copy()
    
    new_point = dataset.pop(i)
    new_name = names2.pop(i)
    new_datapoint = (new_name, new_point)
    trainingset = dataset
    trainingnames = names2
    return trainingset, trainingnames, new_datapoint
    
