#!/usr/bin/python

from __future__ import division
from numpy import add,dot,multiply
from math import sqrt
#from joblib import Parallel, delayed
from Impl_Parser import *
import sys

def constructAdjacencyLists(graph):
  i = 0 #riga
  j = 0 #colonna
  
  lists = [[0 for x in range(len(graph.keys())+1)] for y in range(len(graph.keys())+1)]
                        
  for doc in graph.keys():
    i=0
    for doc2 in graph.keys():
      if doc != doc2:
        if doc2 in graph[doc]:
          lists[i][j] = 1/(len(graph[doc]))
        else:
          lists[i][j] = 0
      else:
        lists[i][j] = 0
      i+=1
    j+=1
  return lists  

def pageRank2(graph,s,step,confidence):
  
  #lists = constructAdjacencyLists(graph)
  """
  for i in range(len(lists)):
    for j in range(len(lists)):
     print lists[i][j],
    print "\n"
  """

  nodes=graph.keys()
  n=len(nodes)
  done = 0
  time = 0
  
  #Initialization
  rank = dict()
  for i in nodes:
    rank[i]=float(1)/n 
  
  tmp=dict()
  while not done and time < step:
    time += 1
    
    for i in nodes:
      tmp[i] = float(1-s)/n #Each nodes receives a share of 1/n with probability 1-s
    
    for i in nodes:
      for j in graph[i]:
        tmp[j] += float(s*rank[i])/len(graph[i]) #Each nodes receives a fraction of its neighbor rank with probability s 
    
    #Computes the distance between the old rank vector and the new rank vector in L_1 norm
    diff = 0
    for i in nodes:
      diff += abs(rank[i]-tmp[i])
      rank[i] = tmp[i]
    
    if diff <= confidence:
      done = 1
    
  return time, rank
