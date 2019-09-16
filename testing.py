#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 20:42:05 2019

@author: rmn
"""

from main import *

points, route, total_distance = main("-f simple.csv -m closest_neighbour".split(" "))
assert total_distance == 30, "on the simple.csv map the closest neighbour method should never cross a diagonal."
# distance function
assert distance(0, 0, 3, 4) == 5
assert distance(*points[0], *points[1]) == 10, "horizontal length calculation check failed"
assert distance(*points[1], *points[0]) == 10, "Order of points shouldn't affect distance calculation"
assert distance(*points[1], *points[2]) == 10, "vertical length calculation check failed"
assert distance(*points[2], *points[1]) == 10, "Order of points shouldn't affect distance calculation"
assert distance(*points[0], *points[2]) == 14.142135623730951, "Diagonal length"
assert distance(*points[2], *points[0]) == 14.142135623730951, "Order of points shouldn't affect distance calculation"
assert distance(*points[1], *points[3]) == 14.142135623730951, "Order of points shouldn't affect distance calculation"
assert distance(*points[3], *points[1]) == 14.142135623730951, "Order of points shouldn't affect distance calculation"
