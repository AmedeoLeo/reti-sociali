from __future__ import division
#!/usr/bin/python 

#The operation of retriving advertisers or documents matching a given query can be executed in two phases:
#in the first phase, we build the necessary data structures;
#in the second phase, we answer to the given query.

#The first phase is usually run only once.
#The data structure that is usually built in this phase is an "inverted index".
#This is a dictionary that for every word (or for every query phrase) mantains a list of
#documents containing that word (query phrase) / advertisers requesting to appear on that word (query phrase).
#In this phase, we assume that there is a database in which we save for each document (advertiser, resp.)
#the link to the document (the name of the advertiser, resp.)
#and the list of word (or phrases) of the document (on which the advertiser request to appear, resp.).
#In the implementations below we assume that the database is a file as follows:
#    nome_adv1 prova,test,prova esame,esame,appello,appello esame
#    nome_adv2 prova,esempio,caso semplice,evidenza
#    nome_adv3 esempio test,esempio esame,esempio prova,esame prova

#The second phase must be executed for any issued query.
#Different strategies are available for this phase:
#either we look for an exact match of the query in the document / advertisers' requests
#or we look for document / advertiser' requests that are "good" match, but not necessarily exact.

###EXACT MATCH###
word_advs = dict()
query_advs = dict()
totalWords = dict()
#We create an inverted index with an entry for every query search on which advertisers requested to appear
def create_query_advs():
    global word_advs
    infile = open("database.txt")
    
    global query_adv
    
    for line in infile:
        name_list = line.split(' ',1) #It splits the line in two elements: the first contains the name of the advertiser, the second a list of query searches
        name=name_list[0]
        queries=name_list[1].split(',') #It splits the list query searches
        
        for query in queries:
            
            query_key = ' '.join(sorted(query.split())) #We reoder every query search so that "prova esame" is the same as "esame prova"
            if query_key not in query_advs.keys():
                query_advs[query_key]=[]
                
            query_advs[query_key].append(name)


#To return an exact match we have to simply return the list that corresponds to the given query in the inverted index    
def exact_match(query):
    global query_advs
    ' '.join(sorted(query.split())) #We reorder the query in the lexicographic order
    
    return query_advs[query]

###BEST MATCH###

#We create an inverted index with an entry for every word of a document or for any word on which advertisers requested to appear
def create_word_advs():
    infile = open("database.txt")
    global word_advs
    global query_advs
    global totalWords
    
    for line in infile:
        name_list = line.split(' ',1)
        name=name_list[0]
        queries=name_list[1].split(',')
        
        
        for i in range(len(queries)):
            query_words=queries[i].split()
            if name not in  totalWords.keys():
                totalWords[name] = 0
            totalWords[name] += len(query_words)
            for word in query_words:
                if word not in word_advs.keys():
                    word_advs[word] = dict()
                if name not in word_advs[word].keys():
                    word_advs[word][name] =  1 #We use a set for avoid repetitions
                    #print "aggiungo chiave ", word
                else:
                    #print word, " gia presente"
                    word_advs[word][name] +=  1
                #It would be possible to save not only the name but also the occurrence of the word in the document / advertiser's request.
                #In this case, we need to associate each name with an accumulator that counts the number of occurrence of the words.
def best_match(query, threshold):
    
    create_word_advs()
    adv_weights = dict()
    best_docs = set()
    global word_advs

    #query_words = query.split()
    #For every word we look at each document in the list and we increment the document's weight
    for word in query:
        for doc in word_advs[word]:
            if doc not in adv_weights.keys():
                adv_weights[doc] = 0
            adv_weights[doc] += word_advs[word][doc] / totalWords[doc]
            #If we would like to count the occurrences, then we must increment the weights not by 1, but by the number of occurrence of that word in the document
            #We use a threshold to choose which document must be returned
            if adv_weights[doc] >= threshold:
				best_docs.add(doc)
    print adv_weights        
    return best_docs    
