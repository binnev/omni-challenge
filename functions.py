#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 15:38:31 2019

@author: rmn
"""

import pandas as pd, matplotlib.pyplot as plt, numpy as np
from math import sqrt
import random


def distance(x1, y1, x2, y2):
    """Euclidian distance between two points"""
    dx = x2 - x1
    dy = y2 - y1
    return sqrt(dx**2 + dy**2)


def get_points_from_route(points, route):
    """Return a copy of the array of points, ordered by the route taken"""
    return np.array([points[i] for i in route])


def plot_points(points):
    fig, ax = plt.subplots(figsize=(8, 8))
    plt.setp(ax, xlabel="x (km)", ylabel="y (km)")
    plt.plot(*points.T, "ok", ms=15, zorder=1)
    for ii, pt in enumerate(points):
        # note: add 1 to point index because user counts from 1
        plt.text(*pt, str(ii+1), color="w", ha="center", va="center",
                 fontweight="bold", zorder=2)
    return fig, ax


def plot_route(ordered_points):
    # plot dashed line for the route
    plt.plot(*ordered_points.T, "--", c="0.5", zorder=-1)
    # add markers for start and end points
    plt.plot(*ordered_points[0], "ob", ms=20)
    plt.plot(*ordered_points[-1], "or", ms=20)


def print_results(ordered_points, route):
    print("Order in which points were visited:")
    template = "{:<10}{:<10}{:<10}"
    print(template.format("Point #", "x coord", "y coord"))
    for ii, pt in zip(route, ordered_points):
        # note: add 1 to point index because user counts from 1
        print(template.format(ii+1, pt[0], pt[1]))
    total_distance = calculate_route_distance(ordered_points)
    print(f"\nTotal length of route (km): {total_distance}")


def calculate_route_distance(ordered_points):
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

#if __name__ == "__main__":
#
#    file = "map_a.csv"
#    # import points
#    points = pd.read_csv(file)
#    points.set_index("index", inplace=True)
#    points = np.array([points.x_coord, points.y_coord]).T
#
#    fig, ax = plot_points(points)
#
#    route = closest_neighbour_route(points, initial_point=0)
#    #route = random_route(points)
#    ordered_points = get_points_from_route(points, route)
#    plot_route(ordered_points)
#    print_results(ordered_points, route)
