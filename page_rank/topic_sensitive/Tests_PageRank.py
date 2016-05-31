#!/usr/bin/python
import timeit
from Impl_PageRank import topicSensitivePageRank

beta=0.80
output = open("time_elapset.txt","w")
while beta<=0.90:
	start_time = timeit.default_timer()
	time, rank = topicSensitivePageRank(beta,75,0)
	elapsed = timeit.default_timer() - start_time
	print >> output,  (str(beta)+" -----> ",time, elapsed)
	beta = beta + 0.01
	
