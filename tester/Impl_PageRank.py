#!/usr/bin/python

from math import sqrt


def pageRank2(old_graph, s,step,confidence):
  #old_graph = readGraph()
  graph=changeGraph(old_graph)
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


  
def readGraph():
    print "-----------READING FILE-----------"
    graph = dict()
    infile = open("graph.txt","r")
    while True:
        line = infile.readline()
        line = line[:-2]
        if not line:
            break
        first_split = line.split(" ")
        #prima split: prendo il topic
        topic = first_split[0]
        if topic not in graph.keys():
            graph[topic]  = dict()
            
        all_urls = first_split[1]
        #seconda split: divido tutti i nodi del grafo

        second_split = all_urls.split("*")
        for elem in second_split:
            #terza split: divido ogni nodo dai suoi vicini
            third_split = elem.split(";")
            url = third_split[0]
            if url not in graph[topic]:
                graph[topic][url] = []
            #se ci sono vicini, li aggiungo al nodo in questione
            neighborhood = third_split[1].split(",")
            if len(neighborhood)>1:
                #print "************************************"
                #print url
                #l'ultimo e' vuoto
                for neighbor in neighborhood[:-1]:
                    if neighbor != url:
                        if neighbor not in graph[topic][url]:
                            #print "-----------------------------------------------"
                            #print neighbor
                            graph[topic][url].append(neighbor)
                        
                        
    """    
    for topic in graph.keys():
        print topic
        line =""
        for url in graph[topic].keys():
            if len(graph[topic][url]):
                line+=url+" ["
                for neigh in graph[topic][url]:
                    line+= neigh+", "
                line+=" ]"
        print line
    """
    
    print ("--------------FINISHED READING-----------")
    return graph
  

def changeGraph(graph):
	new_graph = dict();
	for topic in graph:
		for node in graph[topic]:
			if node not in new_graph:
				new_graph[node]=[]
			for vicino in graph[topic][node]:
				if vicino not in new_graph:
					new_graph[node].append(vicino)
	return new_graph
  
  
  
  
  
