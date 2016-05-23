# -*- coding: utf-8 -*- 
from __future__ import division
from collections import OrderedDict as od

#!/usr/bin/python 

K = 20

###BEST MATCH###

"""Questo metodo restituisce la lista dei primi K documenti in base all'ordinamento dell'inverted index"""
def getFrequentDocs(sorted_db):
    global K
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
def best_match(query, threshold, sorted_db, count_db):
    
    global K
    frequent_docs = getFrequentDocs(sorted_db)
    total_words = count_words(frequent_docs,  count_db)
    
    scores = dict()
    best_docs = dict()
    
    #per ogni documento tra i K documenti ordinati
    for doc in frequent_docs:
        print ("-----------------------------------------------------------")
        print (doc)
        print ("Parole totali "+ str(total_words[doc]))
        #inizializzo
        if doc not in scores.keys():
            scores[doc] = 0
        #query in input
        for q in query:
            for word in q.split():
                print (word)
                print ("Occorrrenze "+ str(count_db[doc][word])) 
            
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
    
    for doc in sorted_docs:
        print (index)
        print (doc)
        print (sorted_docs[doc])
        print ("--------------------------")
        if index == 5:
            break
        index+=1
    
        
    return best_docs   
