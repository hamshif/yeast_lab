
import math

def mean(set):
    sum = 0
    for a in set:
        sum = sum+a
    
    return sum/len(set)


def variance(set):
    mean_ = mean(set)
    squared_differences = []
    
    for a in range(len(set)):
        
        squared_differences.append(pow(mean_-a, 2))
        
    return mean(squared_differences)


def stdev(set):
    
    return math.sqrt(variance(set))
    