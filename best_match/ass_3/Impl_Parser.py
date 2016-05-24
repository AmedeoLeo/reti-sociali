#!/usr/bin/python

from re import findall, sub,  compile
import random
import os
import string
from collections import OrderedDict as od
from nltk.corpus import stopwords
from CSS2 import CSS

K = 12

inverted_db=dict()
count_db = dict()
#Find all links in a web page
def read_links(html):
    #The function findall returns an array of all the occurrence of the searched element in the string given as second parameter
    #The searched element is given as a regular expression (this is indicated by the 'r' written in front of the first parameter)
    #The regular expression that we wrote returns the content of the href parameter of an html anchor
    return findall(r'<a .*?href=[\',\"](.*?)[\',\"].*?>',html)



def clean_text(text):
    
    regex = compile(".*:url\(.*|.*[0-9]*\.?[0-9]*(em|px)|\{.*\}|.*=\".*|[a-zA-Z]*\[.*\]|.*--.*|:&.*|&.*|<.*|.*>|#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})|\/\*.*|.*\*\/")
    regex2 = compile(".*;\/.*|.*{|\..*|.*=\'.*|\(-?.*-.*:.*\)|.*#|#.*|{.*|.*}")
    regex3 = compile("\||-|\\|\.|\:|\/|\"|\'|,|;|_|\*|@|\(|\)|\[|\]|{|}|!|\?|&|%|=|#|\+")
    regex4 = compile(".*:(relative|none|link|visited|top|bottom|left|right)")

    toret = []
    for x in text:
        if not regex.match(x) and not regex4.match(x) and not regex3.match(x) and  not regex2.match(x):
            css = sub(':|;','',x)
            if css not in CSS:
                toret.append(x)
    return toret

#Find all the text in an html page that is not within tags
def read_content(html, url):
    global inverted_db
    global count_db
    cachedStopWords = stopwords.words("english")
    #The function sub substitues any occurrence of the first parameter in the string given as third parameter with an occurrence of the second parameter
    #The first parameter here is given as a regular expression and consists of any html tag
    text = sub(r'<.*?>','',html)
    text = sub('<[^>]*>','',text)
    
    #pulisce le parole non necessarie 
    copy= clean_text(text.split())
    exclude = string.punctuation
    
    for term in copy:
        #ignora keywords CSS
        if term not in CSS:
            #elimina punteggiatura escluso il -
            term = ''.join(ch for ch in term if ch =='-' or ch not in exclude)
            #ignore case
            term = term.lower()
            #ignora le stopwords o le parole di 1 o 2 caratteri
            if term not in cachedStopWords and not term.startswith('url') and len(term) >2:
                
                if term not in inverted_db.keys():
                    inverted_db[term]= set()
                if url not in count_db.keys():
                    count_db[url]=dict()
                if term not in count_db[url]:
                    count_db[url][term] = 0
                #conta le occorrenze della parola nel documento
                count_db[url][term]+=1
                #costruisce l'inverted index
                inverted_db[term].add(url)
        
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
def read_wibbi():
  
    graph=dict()
    
    for filename in os.listdir(os.getcwd()+"/prova/"):
      
        if filename.endswith(".pages"):
            infile = open("prova/"+filename,"r")
            delim=infile.readline().strip() #It will contain the string that wibbi uses a separator
            nl = infile.readline().strip()
            if nl != "0": #The line after the separator will be either the url of the page or "0" if no more pages are present
                url = nl.split()[1]
            html=''
            copy=False
            
            while True:
                line = infile.readline()
                if not line:
                    break
                if line.strip() == delim: #If we find the separator, we have copied the entire html
                    copy=False
                    
                    #We parse the html with the above functions
                    graph[url]=set(read_links(html))
                    read_content(html, url)
                        
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

    printInvertedDB()
    printCountDB()
    
def printInvertedDB():
    output = open("inverted_db.txt","w")
    global inverted_db
    toPrint = ""
    for term in inverted_db.keys():
        toPrint = term + " "
        for doc in inverted_db[term]:
            toPrint += doc + ","
        print >> output, toPrint

def printCountDB():
    output = open("count_db.txt","w")
    global count_db
    toPrint = ""
    for url in count_db.keys():
        toPrint = url + " "
        for elem in count_db[url].keys():
            toPrint += elem + ","
            toPrint += str(count_db[url][elem]) + ";"
        print >> output, toPrint
        
