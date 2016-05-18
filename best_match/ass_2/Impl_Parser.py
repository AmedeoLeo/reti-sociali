#!/usr/bin/python

from re import findall, sub
import random
import os

allgraphs=dict()
#Find all links in a web page
def read_links(html):
    #The function findall returns an array of all the occurrence of the searched element in the string given as second parameter
    #The searched element is given as a regular expression (this is indicated by the 'r' written in front of the first parameter)
    #The regular expression that we wrote returns the content of the href parameter of an html anchor
    return findall(r'<a .*?href=[\',\"](.*?)[\',\"].*?>',html)

#Find all the text in an html page that is not within tags
def read_content(html):
    #The function sub substitues any occurrence of the first parameter in the string given as third parameter with an occurrence of the second parameter
    #The first parameter here is given as a regular expression and consists of any html tag
    text = sub(r'<.*?>','',html)
    text = sub('<[^>]*>','',text)
    return text.split()

#This function removes from the given graph all the edges towards undefined pages
def sanitizer(graph):
    for i in graph.keys():
        neighbors=graph[i].copy()
        for j in neighbors:
            if j not in graph.keys():
                graph[i].remove(j)
    return graph

def connect(graph1, graph2):
    n_links=0
    repeat = True
    while(repeat):
        u = random.choice (graph1.keys())
        v = random.choice (graph2.keys())
        neighbors = graph1[u].copy()
        if v not in neighbors:
            graph1[u].add(v)
            n_links+=1
            if n_links==10:
                repeat=False

    
    
    
#This function reads a wibbi file and returns the resulting graph and the resulting database
#(to be processed by the ranking algorithm and the matching algorithm, respectively)
def read_wibbi(filename):
    infile = open(filename,"r")
    delim=infile.readline().strip() #It will contain the string that wibbi uses a separator
    nl = infile.readline().strip()
    if nl != "0": #The line after the separator will be either the url of the page or "0" if no more pages are present
        url = nl.split()[1]
        
    html=''
    copy=False
    graph=dict()
    db=dict()
    
    while True:
	line = infile.readline()
	if not line:
		break
        if line.strip() == delim: #If we find the separator, we have copied the entire html
            copy=False
            
            #We parse the html with the above functions
            graph[url]=set(read_links(html))
            db[url]=read_content(html)
            
            #We start by reading the url of the next page, if any
            nl = infile.readline().strip()
            if nl != "0":
                url = nl.split()[1]
                
            html=''
            
        #We start to read only when we find the tag "<html"
        ls=line.split()
        if len(ls) > 0 and ls[0] == '<html':
            copy=True
            
        if copy is True:
            html+=line
            
    graph=sanitizer(graph)
    return graph, db


def read_wibbi():
    topic = []
    topic.append("sport")
    topic.append("games")
    topic.append("health")
    topic.append("recreation")
    topic.append("regional")
    topic.append("science")
    topic.append("shopping")
    topic.append("society")
    topic.append("arts")
    topic.append("business")
    topic.append("kids-and-teens")
    topic.append("news")
    topic.append("reference")
    topic.append("shopping")
    topic.append("computers")
    
    topic_graph = dict()
    topic_db = dict()
    index=-1
    for filename in os.listdir(os.getcwd()+"/dataset/"):
      
      if filename.endswith(".pages"):
        index+=1
        infile = open("dataset/"+filename,"r")
        delim=infile.readline().strip() #It will contain the string that wibbi uses a separator
        nl = infile.readline().strip()
        if nl != "0": #The line after the separator will be either the url of the page or "0" if no more pages are present
            url = nl.split()[1]
            
        html=''
        copy=False
       
    
        if topic[index] not in topic_graph.keys():
            topic_graph[topic[index]] = dict()
        
        if topic[index] not in topic_db.keys():
            topic_db[topic[index]] = dict()
           
        while True:
            line = infile.readline()
            if not line:
                break
            if line.strip() == delim: #If we find the separator, we have copied the entire html
                copy=False
                
                #We parse the html with the above functions
                topic_graph[topic[index]][url]=set(read_links(html))
                topic_db[topic[index]][url]=read_content(html)
                
                #We start by reading the url of the next page, if any
                nl = infile.readline().strip()
                if nl != "0":
                    url = nl.split()[1]
                    
                html=''
                
            #We start to read only when we find the tag "<html"
            ls=line.split()
            if len(ls) > 0 and ls[0] == '<html':
                copy=True
                
            if copy is True:
                html+=line
    
    visited=dict()                
    topic_graph[topic[index]]=sanitizer(topic_graph[topic[index]])
    for topic1 in topic_graph.keys():
        if topic1 not in visited.keys():
            visited[topic1]=set()
        for topic2 in topic_graph.keys():
            if topic2 not in visited.keys():
                visited[topic2]=set()
            if topic1 != topic2:
                 if topic2 not in visited[topic1]:
                    print "connetto " + topic1 + " a "+topic2
                    connect(topic_graph[topic1], topic_graph[topic2]) 
                    visited[topic1].add(topic2)
                    visited[topic2].add(topic1)
    return topic_graph, topic_db
