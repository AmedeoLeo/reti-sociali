#!/usr/bin/python

import timeit
from Impl_PageRank import *

start_time = timeit.default_timer()
time2, rank2 = pageRank2(0.85,150,0)
elapsed2 = timeit.default_timer() - start_time

#print(rank2, time2, elapsed2)
print(time2, elapsed2)

for node in rank2:

	print node,str(rank2[node])


