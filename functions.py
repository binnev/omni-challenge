#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 15:38:31 2019

@author: rmn
"""

import pandas as pd, matplotlib.pyplot as plt, numpy as np
from math import sqrt
import random


def import_csv(file):
    points = pd.read_csv(file)
    points.set_index("index", inplace=True)
    return np.array([points.x_coord, points.y_coord]).T


def distance(x1, y1, x2, y2):
    """Euclidian distance between two points"""
    dx = x2 - x1
    dy = y2 - y1
    return sqrt(dx**2 + dy**2)


def generate_random_map(N, width=100):
    xs = [random.randint(0, width) for i in range(N)]
    ys = [random.randint(0, width) for i in range(N)]
    return np.array([xs, ys]).T


def get_points_from_route(points, route):
    """Return a copy of the array of points, ordered by the route taken"""
    return np.array([points[i] for i in route])


def plot_stuff(points, route):
    # plot points
    fig, ax = plt.subplots(figsize=(6, 6))
    plt.setp(ax, xlabel="x (km)", ylabel="y (km)")
    plt.plot(*points.T, "ok", ms=15, zorder=1)
    for ii, pt in enumerate(points):
        # note: add 1 to point index because user counts from 1
        plt.text(*pt, str(ii+1), color="w", ha="center", va="center",
                 fontweight="bold", zorder=2)

    # plot route
    ordered_points = get_points_from_route(points, route)
    plt.plot(*ordered_points.T, "-", c="0.8", zorder=-1)
    # add markers for start and end points
    plt.plot(*ordered_points[0], "ob", ms=20)
    plt.plot(*ordered_points[-1], "or", ms=20)
    return fig, ax


def print_results(points, route, total_distance):
    print("Order in which points were visited:")
    template = "{:<10}{:<10}{:<10}"
    print(template.format("Point #", "x coord", "y coord"))
    ordered_points = get_points_from_route(points, route)
    for ii, pt in zip(route, ordered_points):
        # note: add 1 to point index because user counts from 1
        print(template.format(ii+1, pt[0], pt[1]))
    print(f"\nTotal length of route (km): {total_distance}")


def calculate_route_distance(points, route):

    ordered_points = get_points_from_route(points, route)
    total = 0
    # TODO: use reduce for this?
    for ii in range(1, len(ordered_points)):
        total += distance(*ordered_points[ii], *ordered_points[ii-1])
    return total


def random_route(points, initial_point=None):
    """Generate random route which visits each point exactly once"""
    route = list(range(len(points)))
    random.shuffle(route)
    if initial_point is not None:
        route.remove(initial_point)
        route = [initial_point] + route
    return route


def closest_neighbour_route(points, initial_point=None):
    """Basic heuristic that picks the next point to visit based on how close it
    is to the current point."""

    route = []

    # pick a random start point if none was passed
    if initial_point is None:
        route.append(random.randint(0, len(points)-1))
    else:
        route.append(initial_point)

    # keep choosing points until we've visited them all once
    while len(route) < len(points):
        current_point = points[route[-1]]
        # find the distances to points which haven't already been visited
        distances = [(i, distance(*current_point, *p)) for i, p in enumerate(points) if i not in route]
        # choose the closest point (sort by distance, not point number)
        closest = min(distances, key=lambda x: x[1])
        # append the closest point's number to the route
        route.append(closest[0])

    return route


def analyse_jumps(points, route):
    jumps = []
    for ii in range(1, len(route)):
        current = route[ii]
        previous = route[ii-1]
        temp = {"dist": distance(*points[current], *points[previous]),
                "from": previous, "to": current}
        jumps.append(temp)
    return sorted(jumps, key=lambda x: x["dist"])


def distances_to_neighbours(point_number, points):
    xy = points[point_number]
    distances = [(i, distance(*xy, *p)) for i, p in enumerate(points)]
    # remove current point from list
    distances = list(filter(lambda x: x[0] != point_number, distances))
    return sorted(distances, key=lambda x: x[1])


def closest_neighbour(point_number, points):
    return min(distances_to_neighbours(point_number, points),
               key=lambda x: x[1])


def relocate_point(points, route, point_number, next_to=None):
    # if the user doesn't specify a new neighbour for this point, use the
    # closest point by default
    if next_to is None:
        next_to, _ = closest_neighbour(point_number, points)
#        print(f"I'm using the closest point to point {point_number}: point {next_to}")

    # create a copy of the route with the point removed
    route = route.copy()
    if point_number in route:
        route.remove(point_number)

    # check if it is better to insert the point before or after the closest
    # neighbour
    best_distance = 9e999
    best_route = route
    for insert_position in ("before", "after"):
        trial = route.copy()
        if insert_position == "before":
            trial.insert(trial.index(next_to), point_number)
        else:
            trial.insert(trial.index(next_to)+1, point_number)

#        print(f"inserting point {point_number} {insert_position} point {next_to}:")
        dist = calculate_route_distance(points=points, route=trial)
#        print(f"the distance of this new route is {dist}")
        if dist < best_distance:
            best_distance = dist
            best_route = trial

    return best_route



def smarter_relocate_point(points, route, point_number, consider_N_nearby=5,
                           route_only=False):

    if route_only is False:
        closest_points = distances_to_neighbours(point_number,
                                                 points)[:consider_N_nearby]
    else:
#        print("you want me to relocate this point into the route ONLY")
        distances = distances_to_neighbours(orphan, points)
        closest_points = list(filter(lambda x: x[0] in route,
                                     distances))[:consider_N_nearby]
#        print(f"the closest points are {closest_points}")
#        for p in closest_points:
#            print(f"point {p} in route? {p[0] in route}")

#    print(f"you want to move point {point_number}")
    best_route = route.copy()
    best_distance = calculate_route_distance(points=points, route=route)
    for point, _ in closest_points:
#        print("")
#        print(f"I am going to try moving point {point_number} next to point {point}")
        trial = relocate_point(points, route, point_number, next_to=point)
#        print(trial)
        dist = calculate_route_distance(points=points, route=trial)
#        print(f"This trial route has a length of {dist}")
        if dist < best_distance:
#            print(f"That's better than the previous best! ({best_distance})")
            best_distance = dist
            best_route = trial

    return best_route


def combine_subroutes(subroutes):
    # trivial case -- nothing to rearrange
    if len(subroutes) < 2:
        return subroutes

    combined = []

    # base case -- combine two subroutes
    if len(subroutes) == 2:
        for r1 in (subroutes[0], list(reversed(subroutes[0]))):
            for r2 in (subroutes[-1], list(reversed(subroutes[-1]))):
                combined.append(r1 + r2)

    # recursive case -- more than 2 subroutes
    elif len(subroutes) > 1:
        # consider the first subroute and its reverse
        for r1 in (subroutes[0], list(reversed(subroutes[0]))):
            # compared to all the recombinations of the other subroutes
            for subroute in combine_subroutes(subroutes[1:]):
                # ...and their reverses
                for sub in (subroute, list(reversed(subroute))):
                    combined.append(r1 + sub)

    return combined


def cut_route(points, route, jumps):

    routes = [route.copy()]

    for jump in jumps:
        new_routes = []
        p1, p2 = jump["from"], jump["to"]
        for i, r in enumerate(routes):
            if p1 in r:
                cut = max(r.index(p) for p in (p1, p2))
                new_routes.append(r[:cut])
                new_routes.append(r[cut:])
            else:
                new_routes.append(r)
        routes = new_routes
    return routes


def optimise_route(points, route, shuffle_orphans=True):
    route = route.copy()
    # get top 5 largest jumps
    biggest_jumps = analyse_jumps(points, route)[-5:]
#    print("I'm going to cut the route between")
#    for jump in biggest_jumps:
#        print(f"from {jump['from']} to {jump['to']}")
    # split the route at each jump
    subroutes = cut_route(points, route, biggest_jumps)

    # split up "small" subgroups into ophan points for later relocation
    crit_length = len(points)*.1
    orphans = list(filter(lambda x: len(x) < crit_length, subroutes))
#    print(f"I'm moving these short subroutes to orphans: {orphans}")
    orphans = [item for sublist in orphans for item in sublist]

    # keep long subroutes and recombine them
    subroutes = list(filter(lambda x: len(x) >= crit_length, subroutes))
    trial_routes = combine_subroutes(subroutes)
    distances = [calculate_route_distance(points=points, route=r) for r in trial_routes]
    # pick the shortest route
    ind = np.argmin(distances)
    new_route = trial_routes[ind]
#    print(f"I've recombined the remaining subroutes into a larger route with len {len(new_route)}")

    # relocate the orphan points
    if shuffle_orphans is True:
        random.shuffle(orphans)
    for orphan in orphans:
#        print(f"relocating orphan {orphan}")
        distances = distances_to_neighbours(orphan, points)
        closest_point_in_route, _ = list(filter(lambda x: x[0] in new_route,
                                     distances))[0]
        new_route = relocate_point(points, new_route, orphan,
                                   next_to=closest_point_in_route)
#        print(f"length of route is now {len(new_route)}")

    # smart relocate every point
    for pt in new_route.copy():
        new_route = smarter_relocate_point(points, new_route, pt)

    return new_route


# %%
if __name__ == "__main__":
    pass

    points = generate_random_map(100)
    # old route
#    route = random_route(points, initial_point=0)
    route = closest_neighbour_route(points, initial_point=0)
    total_distance = calculate_route_distance(points, route)
    plot_stuff(points, route)
    plt.title(f"old route ({total_distance} long)")
    #%%
    route = optimise_route(points, route, shuffle_orphans=True)
    total_distance = calculate_route_distance(points, route)
    plot_stuff(points, route)
    plt.title(f"new route ({total_distance} long)")


