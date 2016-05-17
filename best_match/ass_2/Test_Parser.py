#!/usr/bin/python


from Impl_Parser import read_wibbi

graph,db = read_wibbi("../dataset/home.pages")
for i in graph.keys():
    print(i)
    print(graph[i])
    print(db[i])
    input()
