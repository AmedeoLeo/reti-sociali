#!/usr/bin/python

def pageRank2(old_graph, s,step,confidence):
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
    
    diff = 0
    for i in nodes:
      diff += abs(rank[i]-tmp[i])
      rank[i] = tmp[i]
    
    if diff <= confidence:
      done = 1
    
  return time, rank


"""Read and memorizes in data structures the informations contained in the parsed output's file"""
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
        topic = first_split[0]
        if topic not in graph.keys():
            graph[topic]  = dict()
            
        all_urls = first_split[1]

        second_split = all_urls.split("*")
        for elem in second_split:
            third_split = elem.split(";")
            url = third_split[0]
            if url not in graph[topic]:
                graph[topic][url] = []
            #if the current node has neighbours, I will connect them to it
            neighborhood = third_split[1].split(",")
            if len(neighborhood)>1:
              
                #Avoiding the last
                for neighbor in neighborhood[:-1]:
                    if neighbor != url:
                        if neighbor not in graph[topic][url]:
                            graph[topic][url].append(neighbor)
                        
    print ("--------------FINISHED READING-----------")
    return graph
  
""""We need this method to get an useful graph for the basic page rank (without topics)"""
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
  
  
  
  
  
