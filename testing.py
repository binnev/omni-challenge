#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 20:42:05 2019

@author: rmn
"""

from main import *
from functools import reduce

# test outputs on simple map
points, route, total_distance = main("-f simple.csv -m closest_neighbour -i 1".split(" "))
points2, route2, total_distance2 = main("--file simple.csv --method closest_neighbour --initial-point 1".split(" "))
assert points.all() == points2.all(), "long flags should work too"
assert route == route2, "long flags should work too"
assert total_distance == total_distance2, "long flags should work too"
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

# testing function which combines subroutes
l1 = "a _ _ b".upper().split(" ")  # some dummy subroutes with unique endpoints
l2 = "c - d".upper().split(" ")
l3 = "e . . . f".upper().split(" ")
l4 = "g , , , , h".upper().split(" ")
subroutes = l1, l2, l3
routes = combine_subroutes(subroutes)
routes = ["".join(r) for r in routes]
print("routes = ",routes)
tensor = []  # initialise comparison tensor

#for each route
for subroute in subroutes:
    print(f"considering subroute {subroute}")
    matrix = []  # initialise comparison matrix
    # get its endpoints
    endpoints = [subroute[0], subroute[-1]]
    # check that each of its endpoints are adjacent to all the other
    # subroutes' endpoints somewhere in the list of recombined routes...
    other_subroutes = [item for item in subroutes if item != subroute]
    other_endpoints = reduce(lambda a, b: a+b, [[sub[0], sub[-1]] for sub in other_subroutes])
    for endpoint in endpoints:
        print(f"\tconsidering endpoint {endpoint}")
        row = []  # initialise a row of comparisons
        for other in other_endpoints:
            print(f"\t\tis it next to other endpoint {other}?")
            adjacent = False  # assume not adjacent
            # check adjacency
            for route in routes:
                # get the position of the endpoints
                i = route.index(endpoint)
                j = route.index(other)
                if np.abs(i-j) == 1:
                    adjacent = True
                    break  # stop searching routes
            if adjacent:
                print(f"\t\t\tyes! {endpoint} is next to {other} in route:")
                print("\t\t\t", route)
            else:
                print(f"\t\t\tno. {endpoint} is not next to {other} in any of the routes: {routes}")
                raise Exception()
            row.append(adjacent)
        matrix.append(row)
    tensor.append(matrix)
assert np.array(tensor).all() == True
