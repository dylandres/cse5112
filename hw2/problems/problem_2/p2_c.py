'''
Problem 2c
'''

import math
import random
from collections import defaultdict

def d(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def determine_subsquare_for_point(p, delta):
    return p[0] // (delta / 2), p[1] // (delta / 2)

def get_other_subsquares(p):
    other_subsquares = []
    p_x, p_y = p
    for i in range(-2, 3):
        for j in range(-2, 3):
            other_subsquares.append((p_x + i, p_y + j))
    return other_subsquares

def make_dictionary(points, delta):
    subsquare_dict = defaultdict(list)
    for point in points:
        subsquare = determine_subsquare_for_point(point, delta)
        subsquare_dict[subsquare].append(point)
    return subsquare_dict

def better_pair_exists(current_point, other_points, delta, best_pair):
    for other_point in other_points:
        ed = d(current_point, other_point)
        if ed < delta:
            delta = ed
            best_pair = current_point, other_point
            return True, delta, best_pair
    return False, delta, best_pair

def closest_pair(points):
    random.shuffle(points)
    delta = d(points[0], points[1])
    best_pair = points[0], points[1]
    subsquare_dict = make_dictionary([points[0], points[1]], delta)

    for i in range(2, len(points)):
        current_point = points[i]
        subsquare = determine_subsquare_for_point(current_point, delta)

        other_points = []
        other_subsquares = get_other_subsquares(subsquare)
        for point in other_subsquares:
            other_points.extend(subsquare_dict.get(point, []))

        better_pair, delta, best_pair = better_pair_exists(current_point, other_points, delta, best_pair)

        if better_pair:
            subsquare_dict = make_dictionary(points[:i+1], delta)
        else:
            subsquare_dict[subsquare].append(current_point)

    return best_pair
