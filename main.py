#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 18:02:46 2019

@author: rmn
"""

import getopt, sys
from pathlib import Path
from functions import *  # I know this is bad practice, but this library does only one thing...

def check_flag_passed(short, long, flags_passed):
    return (short in flags_passed) or (long in flags_passed)


def enforce_required_flag(short, long, description, flags_passed):
    if not check_flag_passed(short, long, flags_passed):
        print(f"The {description} ('{short}' or '{long}') is required!")
        sys.exit(2)


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

        -i, --initial-point = <integer>
            Force the route generation to start from this point. 

        -s, --save-figure = <filename.ext>
            Save the plot of the route in current working 
            directory. If no filename is given, "route.png"
            will be used. If no extension is specified, png
            will be used. 
            """
    print(helptext)


def main(argv):

    # define expected arguments
    shorts = "hf:m:s:i:"  # colon means parameter required after flag
    longs = ["help", "file=", "method=", "save-figure=", "initial-point="]

    try:
        optargs, _ = getopt.getopt(argv, shorts, longs)
        opts = tuple(opt for opt, arg in optargs)
        args = tuple(arg for opt, arg in optargs)
    except getopt.GetoptError:  # if the user passed unrecognised flags
        print_helptext()        # print the help text
        sys.exit(2)             # and exit with an error

    # if the user passed the help flag, show the help and exit 
    if check_flag_passed("-h", "--help", opts):
        print_helptext()
        sys.exit()  # don't do any other actions if help flag is passed. 

    # enforce required flags
    required = [("-f", "--file", "input file flag"),]
    for flag in required:
        enforce_required_flag(*flag, opts)

    # default values
    method = "random"
    save_figure = False
    initial_point = None

    # parse flags
    for opt, arg in optargs:
        if opt in ("-f", "--file"):
            file = arg
        elif opt in ("-m", "--method"):
            method = arg
        elif opt in ("-s", "--save-figure"):
            save_figure = True
            figure_filename = arg
        elif opt in ("-i", "--initial-point"):
            if not arg.isdigit():
                print("The initial point must be an integer"
                      f"(you entered {arg}")
            initial_point = int(arg) - 1  # user counts from 1
        else:
            print(f"I don't recognise option {opt, arg}")

    # check file exists
    file = Path(file)
    if not file.is_file():
        print(f"This file doesn't exist: {file.as_posix()}")

    # import points
    points = pd.read_csv(file)
    points.set_index("index", inplace=True)
    points = np.array([points.x_coord, points.y_coord]).T

    # choose route 
    if method == "random":
        route = random_route(points, initial_point)
    elif method == "closest_neighbour":
        route = closest_neighbour_route(points, initial_point)
    else:
        print(f"I don't recognise that method: {method}")
        sys.exit()

    ordered_points = get_points_from_route(points, route)

    # show results
    fig, ax = plot_points(points)
    plot_route(ordered_points)
    print_results(ordered_points, route)

    # save the plot of the route
    if save_figure:
        if figure_filename.strip() == "":
            figure_filename = "route.png"
        else:
            if Path(figure_filename).suffix == "":
                figure_filename = figure_filename + ".png"
        plt.tight_layout()
        fig.savefig(figure_filename)

    return points, route

if __name__ == "__main__":
    main(sys.argv[1:])