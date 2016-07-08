#!/usr/bin/python

def topicSensitivePageRank(graph, beta, step, confidence):
    #Initialization
    rank = dict()
    done = 0
    time = 0
    
    tmp=dict()
    print "-------------STARTING PAGE RANK-------------"

    for topic in graph.keys():
	
        print ("CURRENT TOPIC:"+topic)
        s  =len(graph[topic])
        if topic not in rank.keys():
            rank[topic] = dict()
       
        for node in graph[topic]:

            if node not in rank[topic].keys():
                rank[topic][node]=0
            rank[topic][node] = float(1)/s
	    	 
  	time=0
	done=0
        while not done and time < step:
            time += 1
            if topic not in tmp.keys():
                tmp[topic] = dict()
            
            for node in graph[topic]:
                if node not in tmp[topic]:
                    tmp[topic][node]=0 
                tmp[topic][node] = float(1-beta)/s #Each nodes receives a share of 1/s with probability 1-beta
               
            for current in graph[topic]:
                for neighbor in graph[topic][current]:	

                    if neighbor not in tmp[topic]:
                        tmp[topic][neighbor] = float(1-beta)/s
                    tmp[topic][neighbor] += float(beta*rank[topic][current]) / len(graph[topic][current])  #Each nodes receives a fraction of its neighbor rank
            diff = 0

            for currTopic in graph.keys():
                if currTopic == topic:
		    for node in graph[topic]:
			diff += abs(rank[topic][node]-tmp[topic][node])
			rank[topic][node] = tmp[topic][node]
			if diff <= confidence:
			    done = 1

		else:
		    for node in graph[currTopic]:
			if node not in graph[topic]:
			    if currTopic not in rank.keys():
				rank[currTopic] = dict()
			    if node in tmp[topic].keys():
				if node not in rank[currTopic].keys():
				    rank[currTopic][node] = tmp[topic][node]
				    tmp[topic][node] = 0
				    diff += abs(rank[currTopic][node]-tmp[topic][node])

				    if diff <= confidence:
					done = 1
	
    print("PAGE RANK COMPLETE")

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
            neighborhood = third_split[1].split(",")
            if len(neighborhood)>1:
             
                for neighbor in neighborhood[:-1]:
                    if neighbor != url:
                        if neighbor not in graph[topic][url]:
                            graph[topic][url].append(neighbor)
    
    print ("--------------FINISHED READING-----------")
    return graph
