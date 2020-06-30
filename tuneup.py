#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment

Use the timeit and cProfile libraries to find bad code.
"""

__author__ = "DJJD2150, Kano Marvel, David Richardson, Mike A., Janell Huyck"
"""Got help from websites https://zapier.com/engineering/profiling-python-boss/, 
https://pymotw.com/2/profile/"""


import cProfile
import pstats
import functools
import timeit


def profile(func):
    """A cProfile decorator function that can be used to
    measure performance.
    """
    # Be sure to review the lesson material on decorators.
    # You need to understand how they are constructed and used.
    def c_profile(*args, **kwargs):
        # Creates a cProfile object inside the decorator's inner function.
        profile = cProfile.Profile()
        try:
            # Enables the cProfile object to start its timers
            profile.enable()
            # Invokes the original function, passing all args and kwargs to the original function
            result = func(*args, **kwargs)
            # Disables the cProfile object after the original function returns
            profile.disable()
            return result
        finally:
            # Creates a Stats object that collects stats from the cProfile object
            stats = pstats.Stats(profile)
            # Sort the statistics by the cumulative time they take to run
            stats.sort_stats('cumulative')
            # Print the stats
            stats.print_stats()
    return c_profile


def read_movies(src):
    """Returns a dictionary of movie titles."""
    # Shows which file is being read
    print(f'Reading file: {src}')
    # opens read-only version of file listed in the function's argument
    with open(src, 'r') as f:
        # creates an empty dictionary for the listed movies to go into
        # the values will be the amount of times each movie title shows up
        movies_dict = {}
        # splits the movie list into lines
        movies = f.read().splitlines()
        # loops through each individual movie
        for movie in movies:
            # makes the titles lower case
            movie = movie.lower()
            # gets the movies assigns them to the movies dictionary, while assigning
            # them as keys and giving them an initial value of 0
            movie_value = movies_dict.get(movie, 0)
            # conditional statement increases the value of the movie
            # the elif statement is for duplicates 
            if movie_value == 0:
                movies_dict[movie] = 1
            elif movie_value != 0:
                movies_dict[movie] += 1
        return movies_dict


@profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from an src list."""
    # gets the read_movies function and assigns it to a variable
    movies_dict = read_movies(src)
    # creates an empty list to place duplicate movie titles in
    duplicates = []
    # assigns the movies dictionary's values and keys to variables
    movie_value = movies_dict.values()
    movie_key = movies_dict.keys()
    # loop appends any duplicate movie titles to the duplicates list
    for movie_key, movie_value in movies_dict.items():
        if movie_value > 1:
            duplicates.append(movie_key)
    return duplicates


def timeit_helper():
    """Part A: Obtain some profiling measurements using timeit."""
    # checks the time it takes for the find_duplicate_movies function to run
    # when the "movies.txt" file is its argument
    t = timeit.Timer(stmt="find_duplicate_movies('movies.txt')", 
    setup="from tuneup import find_duplicate_movies")
    # runs 35 times total (7 repeats * 5 runs per repeat) and assigns the resulting
    # value to a variable, then returns the best time
    result = t.repeat(repeat=7, number=5)
    return min(result) / 5


def main():
    """Computes a list of duplicate movie entries."""
    # assigns find_duplicate_movies to a local variable in the main function
    result = find_duplicate_movies('movies.txt')
    # prints the best time using the timeit_helper function within the string below
    print(f'The best time across 7 repeats of 5 runs per repeat: {timeit_helper()} seconds.')
    # prints the amount of duplicate movies put into the list within the string below
    print(f'Found {len(result)} duplicate movies:')
    # prints the duplicate movies
    print('\n'.join(result))


if __name__ == '__main__':
    main()
