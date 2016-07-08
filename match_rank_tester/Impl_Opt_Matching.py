# -*- coding: utf-8 -*- 
from __future__ import division
from collections import OrderedDict as od
from decimal import *


###OPTIMIZED BEST MATCH###

"""Threshold K, we assume that it is fixed: K=60"""
def countK():
   # return (len(count_db.keys())*0.2)/100
   return 60

"""This method returns  a list consisting of the first K documents based on the inverted index sorting"""
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
        
"""This method computes the total number of words for each document"""
def count_words(frequent_docs, count_db):
    total_words=dict()
    for doc in count_db.keys():
        if doc not in total_words:
            total_words[doc]=0
        for word in count_db[doc].keys():
            total_words[doc]+=count_db[doc][word]
    return total_words




def opt_best_match(inverted_db, query, threshold):
   
    sorted_db = dict()
    query_db = dict()    

    for q in query:
        for term in q.split():
            if term in inverted_db:
                if term not in query_db:
                    query_db[term]= dict() 
                query_db[term]=inverted_db[term]


    temp =  sorted(query_db, key=lambda x:len(query_db[x]), reverse=True)
    sorted_db = od((x, query_db[x]) for x in temp)

    K = countK()
    best_docs = dict()
    best_docs2 = dict()
    count=0
    
    for parola in sorted_db:
        for doc in sorted_db[parola]:
            if count<K:
                if doc not in best_docs:
                    best_docs[doc]=0
                    count+=1
                best_docs[doc]+=sorted_db[parola][doc]
            else:
                if doc in best_docs:
                    best_docs[doc]+=sorted_db[parola][doc]

    #sorting
    temp =  sorted(best_docs, key=lambda x: best_docs[x], reverse=True)
    sorted_docs = od((x, best_docs[x]) for x in temp)

    count =0
    for doc in sorted_docs:
        if count < 20:
            count+=1
            if doc not in best_docs2:
                best_docs2[doc]=0
            best_docs2[doc]=sorted_docs[doc]

    temp2 =  sorted(best_docs2, key=lambda x: best_docs2[x], reverse=True)
    best_docs = od((x, best_docs[x]) for x in temp2)
	
    return best_docs  


"""Read and memorizes in data structures the informations contained in the parsed output's file"""
def readInvertedDB():
    inverted_db = dict()
    infile = open("inverted_db.txt","r")

    while True:
        line = infile.readline()
        line = line[:-2]
        if not line:
            break
        
        first_split = line.split(" ")
        term = first_split[0]
        urls = first_split[1]
        second_split = urls.split(";")
         
        if term not in inverted_db.keys():
            inverted_db[term] = dict()
        for couple in second_split:
            current = couple.split(",")
            url  = current[0]
            frequency = float(current[len(current)-1])
            if url not in inverted_db[term].keys():
                inverted_db[term][url]=0
            inverted_db[term][url] = frequency
    
    print ("--------------------READ INVERTED DB COMPLETED-------------")
    return inverted_db
