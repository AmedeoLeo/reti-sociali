from __future__ import division
#!/usr/bin/python 

word_advs = dict()
query_advs = dict()
totalWords = dict()

###BEST MATCH###

#We create an inverted index with an entry for every word of a document or for any word on which advertisers requested to appear
def create_word_advs():
    infile = open("count_db.txt")
    global word_advs
    global query_advs
    global totalWords
    
    for line in infile:
        line = line[:-2]
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

def basic_best_match(query, threshold):
    
    create_word_advs()
    adv_weights = dict()
    best_docs = dict()
    global word_advs

    #query_words = query.split()
    #For every word we look at each document in the list and we increment the document's weight
    for word in query.keys():
        for doc in word_advs[word]:
            if doc not in adv_weights.keys():
                adv_weights[doc] = 0
            adv_weights[doc] += word_advs[word][doc] / totalWords[doc]
            #If we would like to count the occurrences, then we must increment the weights not by 1, but by the number of occurrence of that word in the document
            #We use a threshold to choose which document must be returned
            #if adv_weights[doc] >= threshold:
            #best_docs.add(doc)
            

    #ordino in maniera decrecente
    temp =  sorted(adv_weigths, key=lambda x: adv_weigths[x], reverse=True)
    sorted_docs = od((x, adv_weigths[x]) for x in temp)
    index =1

    #output = open("scores.txt","w")

    for doc in sorted_docs:
        #print >> output, index
        #print >> output, doc
        #print >> output, sorted_docs[doc]
        #print >> output, "--------------------------"

        if doc not in best_docs.keys():
           best_docs[doc] = 0
        best_docs[doc] = sorted_docs[doc]
        
        if index == 20:
            break
        index+=1
                
    return best_docs

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
        terms = first_split[1]
        second_split = terms.split(",")

        if doc not in count_db.keys():
            count_db[doc] = set()
         
        for word in second_split:
            if word not in count_db[doc].keys():
                count_db[doc].append(word)
    
    return count_db

