"""Some basic functions for the processing of data.
"""
from math import sqrt
from collections.abc import Iterable

def covariance(param1: list, param2: list) -> float:
    """Return the covariance of parameter lists param1 and param2.        
    
    Assumption: param1 and param2 contain numbers and are of equal length.
    
    :param param1: List of parameters to be compared.
    :param param2: List of parameters to compare with.
    :return: covariance of param1 and param2.
    
    >>> covariance([1, 3, 5, 11, 0, 4], [2, 6, 2, 78, 1, 4])
    106.4
    >>> covariance([1], [1, 2])
    Traceback (most recent call last):
        ...
    AssertionError: Parameter lists must be of the same length.    
    """
    assert len(param1) == len(param2), "Parameter lists must be of the same length."
    
    n = len(param1)
    
    mean1 = sum(param1)/n
    mean2 = sum(param2)/n
    
    sumDif = 0
    for i in range(n):
        dif1 = param1[i] - mean1
        dif2 = param2[i] - mean2
        a = dif1*dif2
        sumDif += (a)
        
    covar = sumDif/n
    
    return covar


def standardDeviation(param: list) -> float:
    """Calculate the standard deviation of a list of measurements.
    
    :param param: list of data of which the std needs to be calculated.
    :returns: standard deviation of param.
    :examples:
    >>> standardDeviation([2, 4, 4, 4, 5, 5, 7, 9])
    2.0
    """
    N = len(param)
    mean = sum(param)/N
    sqDevs = []
    for thing in param:
        sqDev = (mean - thing)**2
        sqDevs.append(sqDev)
    variance = sum(sqDevs)/N
    std = sqrt(variance)
    return std 


def correlationCoefficient(param1: Iterable, param2: Iterable) -> float:
    """Calculate the Pearson correlation coefficient of two parameters.
    
    :examples:
    >>> correlationCoefficient([1, 2, 3, 5, 8], [0.11, 0.12, 0.13, 0.15, 0.18])
    1.0
    """
    corCoef = covariance(param1, param2)/(standardDeviation(param1)*standardDeviation(param2))
    return corCoef
