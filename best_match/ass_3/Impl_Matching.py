# -*- coding: utf-8 -*- 
from __future__ import division
from collections import OrderedDict as od

#!/usr/bin/python 



###BEST MATCH###

def countK(count_db):
    return (len(count_db.keys())*0.2)/100

"""Questo metodo restituisce la lista dei primi K documenti in base all'ordinamento dell'inverted index"""
def getFrequentDocs(sorted_db,K):
    check=0
    done = False
    frequent_docs = set()
    for term in sorted_db:
        if done == False:
            for doc in sorted_db[term]:
                if doc not in frequent_docs:
                    frequent_docs.add(doc)
                    check+=1
                if check == K:
                    done =True
                    break
    return frequent_docs
        
"""Metodo che calcola le parole totali contenute in ogni documento"""
def count_words(frequent_docs, count_db):
    total_words=dict()
    for doc in count_db.keys():
        if doc not in total_words:
            total_words[doc]=0
        for word in count_db[doc].keys():
            total_words[doc]+=count_db[doc][word]
    return total_words

"""Ottimizzazione al best match classico: per ogni query in input ottimizza solo i primi K documenti 
ricavati tramite inverted index"""
def best_match(query, threshold):

    inverted_db = readInvertedDB()
    count_db = readCountDB()
    #ordina l'inverted index in ordine decrescente
    temp =  sorted(inverted_db, key=lambda x: len(inverted_db[x]), reverse=True)
    sorted_db = od((x, inverted_db[x]) for x in temp)
        
    K = countK(count_db)
    frequent_docs = getFrequentDocs(sorted_db,K)
    total_words = count_words(frequent_docs,  count_db)
    
    scores = dict()
    best_docs = dict()

    for doc in count_db.keys():
        print doc
        for word in count_db[doc].keys():
            if doc in total_words.keys():
                print word
                print count_db[doc][word] / total_words[doc]
                print "---------------------------"
    
    #per ogni documento tra i K documenti ordinati
    for doc in frequent_docs:
        #print ("-----------------------------------------------------------")
        #print (doc)
        #print ("Parole totali "+ str(total_words[doc]))
        #inizializzo
        if doc not in scores.keys():
            scores[doc] = 0
        #query in input
        for q in query:
            for word in q.split():
                #print (word)
                #print ("Occorrrenze "+ str(count_db[doc][word])) 
            
                # se la query in input non è presente nel doc aggiungo zero
                if word not in count_db[doc].keys():
                    scores[doc] += 0
                #altrimenti aggiorno in base alla frequenza: [occorrenze parola nel doc] / [parole totali nel doc]
                else:
                    scores[doc] += count_db[doc][word] / total_words[doc]

              
    #ordino in maniera decrecente
    temp =  sorted(scores, key=lambda x: scores[x], reverse=True)
    sorted_docs = od((x, scores[x]) for x in temp)
    index =1

    output = open("scores.txt","w")

    for doc in sorted_docs:
        print >> output, index
        print >> output, doc
        print >> output, sorted_docs[doc]
        print >> output, "--------------------------"
        if index == 20:
            break
        index+=1
            
    return best_docs   

    
def readInvertedDB():
    inverted_db = dict()
    infile = open("inverted_db.txt","r")

    while True:
        line = infile.readline()
        line = line[:-2]
        if not line:
            break
        
        split = line.split(" ")
        term = split[0]
        urls = split[1]

        if term not in inverted_db.keys():
            inverted_db[term] = set()

        urlsplit = urls.split(",")
        for i in range(len(urlsplit)):
            inverted_db[term].add(urlsplit[i])

    return inverted_db

def readCountDB():
    count_db = dict()
    infile = open("count_db.txt","r")

    while True:
        line = infile.readline()
        line = line[:-2]
        if not line:
            break
        
        first_split = line.split(" ")
        url = first_split[0]
        terms = first_split[1]

        second_split = terms.split(";")

        if url not in count_db.keys():
            count_db[url] = dict()
            
        for couple in second_split:
            current = couple.split(",")
            term = current[0]
            occurrency = int(current[1])

            if term not in count_db[url].keys():
                count_db[url][term] = 0

            count_db[url][term] = occurrency
        
    return count_db
