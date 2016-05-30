#!/usr/bin/python

import math
from math import *

def topicSensitivePageRank(beta, step, confidence):
    
    graph = readGraph()
    #Initialization
    rank = dict()
    done = 0
    time = 0
    tmp = dict()
    print "-------------STARTING PAGE RANK-------------"
    output2 = open("details.txt","w")

    for topic in graph.keys():
        print >> output2, "CURRENT TOPIC:"+topic
        s = len(graph[topic])
        print s
        if topic not in rank.keys():
            rank[topic] = dict()
       
        for node in graph[topic].keys():

            if node not in rank[topic].keys():
                rank[topic][node]=0
            #if rank[topic][node] != 0:
            #    print "SOMMO AL VECCHIO VALORE!"
            #print >> output2, "SOMMO 1/s a " + node
            rank[topic][node] += float(1)/s

        time = 0
        done = 0
        while not done and time < step:
            time += 1
        
            if topic not in tmp.keys():
                tmp[topic] = dict()
            
            for node in graph[topic].keys():
                if node not in tmp[topic].keys():
                    tmp[topic][node]=0
                #probabilita che un random surfer segua un link casuale
                #print >> output2, "ASSEGNO 1-b/s a " + node
                tmp[topic][node] = float(1-beta)/s #Each nodes receives a share of 1/n with probability 1-beta
    
            #si cicla su tutti i nodi della rete. Se il nodo corrente appartiene al topic corrente si somma un extra (1-beta)/|S|
            #altrimenti si aggiorna sommando beta per il precedente vettore rank
            
            for current in graph[topic].keys():
                for neighbor in graph[topic][current]:
                    if neighbor not in tmp[topic].keys():
                        tmp[topic][neighbor] = 0
                    print >> output2, "AGGIORNO " + neighbor + " con " + current
                    tmp[topic][neighbor] += float(beta*rank[topic][current])  #Each nodes receives a fraction of its neighbor rank with probability beta
               
            #Computes the distance between the old rank vector and the new rank vector in L_1 norm
            diff = 0
            
            for currTopic in graph.keys():
                if currTopic == topic:
                    for node in graph[topic]:
                        diff += abs(rank[topic][node]-tmp[topic][node])
                        rank[topic][node] = tmp[topic][node]
                        #if diff <= confidence:
                            #done = 1
                else:
                    for node in graph[currTopic]:
                        if node not in graph[topic]:
                            if currTopic not in rank.keys():
                                rank[currTopic] = dict()
                            if node in tmp[topic].keys():
                                if node not in rank[currTopic].keys():
                                    rank[currTopic][node] = 0
                                diff += abs(rank[currTopic][node]-tmp[topic][node])
                                rank[currTopic][node] = tmp[topic][node]

                                #print "sto aggiornando: ",  node,  str(tmp[topic][node])
                                #if diff <= confidence:
                                    #done = 1
                #spostato
                if diff <= confidence:
                    done = 1
    print("PAGE RANK COMPLETE")
    print("-----------PRINTING-----------")
    output = open("test.txt","w")
    for topic in rank.keys():
        print >> output, topic
        for node in rank[topic].keys():
            #if isinf(rank[topic][node]):
            print >> output, node + " "+ str(rank[topic][node])
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
               
                #l'ultimo e' vuoto
                for neighbor in neighborhood[:-1]:
                    if neighbor != url:
                        if neighbor not in graph[topic][url]:
                            graph[topic][url].append(neighbor)
    """
    details2 = open("details2.txt","w")   
    for topic in graph.keys():
        print >> details2, topic
        line =""
        for url in graph[topic].keys():
            if len(graph[topic][url]):
                line+=url+" ["
                for neigh in graph[topic][url]:
                    line+= neigh+", "
                line+=" ]"
        print >> details2, line
    """
    
    print ("--------------FINISHED READING-----------")
    return graph
