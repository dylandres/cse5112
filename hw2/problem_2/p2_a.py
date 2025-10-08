'''
Problem 2a
'''

import math

def d(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def closest_pair(points):
    closest = float('inf')
    closest_points = None
    for i in range(len(points)):
        for j in range(len(points)):
            if i == j:
                continue
            point1 = points[i]
            point2 = points[j]
            ed = d(point1, point2)
            if ed < closest:
                closest_points = (point1, point2)
                closest = ed
    return closest_points
