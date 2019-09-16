#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 18:02:46 2019

@author: rmn
"""

import getopt
from functions import *  # I know this is bad practice, but this library does only one thing...

def print_helptext():
    helptext = """USAGE:
        -h, --help
            Show this help text.

        -f, --file = <file>
            Path to the CSV file you want to use.
            Required.

        -m, --method = <method name> 
            Name of the route-finding method you want to use. 
            Available methods are: 
            - "random"
            - "closest_neighbour"

            Defaults to "random". 

        -s, --save-figure
            Save the plot of the route as route.png in 
            current working directory. 
            """
    print(helptext)


def main():
    file = "map_c.csv"
    # import points
    points = pd.read_csv(file)
    points.set_index("index", inplace=True)
    points = np.array([points.x_coord, points.y_coord]).T

    fig, ax = plot_points(points)

    route = closest_neighbour_route(points)
    #route = random_route(points)
    ordered_points = get_points_from_route(points, route)
    plot_route(ordered_points)
    print_results(ordered_points, route)


if __name__ == "__main__":
    main()