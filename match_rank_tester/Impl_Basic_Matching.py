from __future__ import division
from collections import OrderedDict as od

word_advs = dict()
query_advs = dict()
totalWords = dict()

###BEST MATCH###
                  
"""This method returns a dictionary consisting of all the terms' frequencies"""
def create_word_advs(count_db):
	frequencies = dict()
	for doc in count_db:
		if doc not in frequencies:
			frequencies[doc] = dict()
		for word in count_db[doc]:
			occurency = count_db[doc].count(word)
			if word not in frequencies[doc]:
				frequencies[doc][word] = occurency
	return frequencies


def basic_best_match(query, threshold):
    
    count_db = readCountDB()
    frequencies = create_word_advs(count_db)
    scores = dict()
    best_docs = dict()
  
    for q in query:
        for term in q.split():
            for doc in frequencies:
                totalWords = len(count_db[doc])
                if doc not in scores:
                    scores[doc] = 0
                if term not in frequencies[doc]:
                    scores[doc] += 0
                else:
                    scores[doc] += frequencies[doc][term]/totalWords
    


    #sorting
    temp =  sorted(scores, key=lambda x: scores[x], reverse=True)
    sorted_docs = od((x, scores[x]) for x in temp)
    index =1


    for doc in sorted_docs:
      
        if doc not in best_docs.keys():
           best_docs[doc] = 0
        best_docs[doc] = sorted_docs[doc]
        
        if index == 20:
            break
        index+=1
    temp2 =  sorted(best_docs, key=lambda x: best_docs[x], reverse=True)
    best_docs2 = od((x, best_docs[x]) for x in temp2)
    return best_docs2

"""Read and memorizes in data structures the informations contained in the parsed output's file"""
def readCountDB():
    count_db = dict()
    infile = open("count_db.txt","r")

    while True:
        line = infile.readline()
        line = line[:-2]
        if not line:
            break
        
        first_split = line.split(" ")
        doc = first_split[0]
        if doc not in count_db.keys():
            count_db[doc] = []
             
        if len(first_split) > 1:
            terms = first_split[1]
            second_split = terms.split(",")

            for word in second_split:
                if word not in count_db[doc]:
                    count_db[doc].append(word)
        
    return count_db

