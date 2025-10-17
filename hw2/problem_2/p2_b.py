'''
Problem 2b
'''

import math

def d(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def closest_pair_brute_force(p_x, p_y):
    closest = float("inf")
    closest_points = None
    for i in range(len(p_x)):
        for j in range(i + 1, len(p_x)):
            point1 = p_x[i]
            point2 = p_x[j]
            ed = d(point1, point2)
            if ed < closest:
                closest_points = (point1, point2)
                closest = ed
    return closest_points

def compare_to_next_15_points(s_y):
    closest = float("inf")
    closest_points = None
    for i in range(len(s_y)):
        other_15 = min(i + 16, len(s_y))
        for j in range(i + 1, other_15):
            ed = d(s_y[i], s_y[j])
            if ed < closest:
                closest_points = (s_y[i], s_y[j])
                closest = ed
    return closest_points, closest

def closest_pair_rec(p_x, p_y):
    if len(p_x) <= 3:
        return closest_pair_brute_force(p_x, p_y)

    q_x = [p for i, p in enumerate(p_x) if i < len(p_x) // 2]
    q_y = [p for p in p_y if p in q_x] 
    r_x = [p for i, p in enumerate(p_x) if i >= len(p_x) // 2]
    r_y = [p for p in p_y if p in r_x]

    (q_0, q_1) = closest_pair_rec(q_x, q_y)
    (r_0, r_1) = closest_pair_rec(r_x, r_y)

    q_dist = d(q_0, q_1)
    r_dist = d(r_0, r_1)
    delta = q_dist if q_dist < r_dist else r_dist
    x_star = q_x[-1][0]
    L = x_star
    
    s_y = [p for p in p_y if abs(p[0] - L) <= delta]
    s_pair, s_dist = compare_to_next_15_points(s_y)

    if s_dist < delta:
        return s_pair
    elif q_dist < r_dist:
        return q_0, q_1
    else:
        return r_0, r_1

def closest_pair(points):

    p_0 = sorted(points, key=lambda point: point[0])
    p_1 = sorted(points, key=lambda point: point[1])

    pair = closest_pair_rec(p_0, p_1)
    return pair[0], pair[1]
