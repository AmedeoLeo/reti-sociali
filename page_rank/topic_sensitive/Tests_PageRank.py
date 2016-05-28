#!/usr/bin/python
import timeit
from Impl_PageRank import topicSensitivePageRank



# Graph is represented with its adjacency lists
topic = ["topic1", "topic2"]

graph = dict()
graph[topic[0]] = dict()
graph[topic[1]] = dict()


simple = dict()
simple['x'] = {'y','z','w'}
simple['y'] = {'x','w', 'x2'}
simple['z'] = {'x', 'y2'}
simple['w'] = {'y','z'}

simple2 = dict()
simple2['x2'] = {'y2','w2', 'k2', 'y'}
simple2['y2'] = {'x2','w2', 'z'}
simple2['w2'] = {'y2'}
simple2['k2'] = {'x2'}

graph[topic[0]] = simple
graph[topic[1]] = simple2
"""
for t in graph.keys():
    print t
    for node in graph[t]:
        print node
        print graph[t][node]
"""

start_time = timeit.default_timer()
time, rank = topicSensitivePageRank(0.85,75,0)
elapsed = timeit.default_timer() - start_time

        
print(time, elapsed)
