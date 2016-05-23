#!/usr/bin/python

import timeit
from Impl_Parser import *
from Impl_PageRank import *

# Graph is represented with its transition matrix
#simple = ([0, 1/2, 1, 0], [1/3, 0, 0, 1/2], [1/3, 0, 0, 1/2], [1/3, 1/2, 0, 0])

graph = read_wibbi()
time, rank = pageRank2(graph, 0.85, 75, 0)
print time
print rank

"""
start_time = timeit.default_timer()
time1, rank1 = pageRank1(simple,0.85,75,0)
elapsed1 = timeit.default_timer() - start_time

print(rank1, time1, elapsed1)
"""
