import timeit
import sys
import os
from Impl_Topic_Sensitive_PageRank import readGraph,  topicSensitivePageRank
from Impl_Opt_Matching import readInvertedDB,  opt_best_match
from Impl_Basic_Matching import basic_best_match
from Impl_PageRank import pageRank2
from collections import OrderedDict as od

#query=["auxiliary",  "chair", "champions league"]
#query=["medicine has existed for thousands of years"]
#query=["yogurt is produced using a culture of Lactobacillus delbrueckii subsp"]
#query=["yogurt medicine"]
#query = ["yogurt medicine"]
query = ["yogurt"]
#query = ["Modern English has little inflection compared with many other languages, and relies more on auxiliary verbs"]
#query = ["The basic aim of the journal is to carry out researches on different disciplines of social sciences, more specifically on cultural and sport studies. Through the production of scientific researches, IntJSCS hopes to contribute to the internationalization process of ISCSA. Therefore the journal accepts researches in English language from all over the world."]

"""Executes the basic best match algorithm"""
def run_basic_best_match():
    output = open("20_basic_best_match.txt", "w")
    print >> output, "///////////////////////// Basic Best Match /////////////////////////"
    print >> output, "Query utilizzate: ", query
    threshold=0
    print >> output, "Threshold: ", str(threshold)
    
    start_time = timeit.default_timer()
    basic_best_docs = basic_best_match(query,threshold)
    basic_match_elapsed = timeit.default_timer() - start_time
    
    print >> output, "Migliori 20 documenti: "
    for doc in basic_best_docs:
    	print >> output,doc,"---->",str(basic_best_docs[doc])
    print >> output, "Tempo impiegato: ", str(basic_match_elapsed)
    
    return basic_best_docs
    
"""Executes the optimized best match algorithm"""    
def run_opt_best_match(inverted_db):
    output = open("20_opt_best_match.txt", "w")
    print >> output, "///////////////////////// Optimized Best Match /////////////////////////"
    print >> output, "Query utilizzate: ", query
    threshold=0
    print >> output, "Threshold: ", str(threshold)
    
    start_time = timeit.default_timer()
    opt_best_docs = opt_best_match(inverted_db,query,threshold)
    opt_match_elapsed = timeit.default_timer() - start_time

    print >> output, "Migliori 20 documenti: "
    for doc in opt_best_docs:
    	print >> output,doc,"---->",str(opt_best_docs[doc])
    print >> output, "Tempo impiegato: ", str(opt_match_elapsed)
    
    return opt_best_docs

"""Executes the basic page rank algorithm"""    
def run_page_rank(graph,output,b,i,confidence):
    print >> output, "///////////////////////// Page Rank /////////////////////////"
    print >> output, "///////////////////////// Iterazione: ",i," /////////////////////////"
    
    beta = b
    step = 100
    #confidence = 0.1

    print >> output, "Beta: ", str(beta)
    print >> output, "Step massimi: ", str(step)
    print >> output, "Confidence: ", str(confidence)
    
    start_time = timeit.default_timer()
    steps,  ranks = pageRank2(graph, beta, step,confidence)
    page_rank_elapsed = timeit.default_timer() - start_time

    print >> output, "Step utilizzati: ", str(steps)
    #for doc in ranks:
	    #print >> output, "Ranks: ", doc, "--->", ranks[doc]
    print >> output, "Tempo impiegato: ", str(page_rank_elapsed)
    
    return ranks

"""Executes the topic sensitive page rank algorithm"""    
def run_topic_sensitive_page_rank(graph,output,b,i,confidence):
    print >> output, "///////////////////////// Topic Sensitive Page Rank /////////////////////////"
    print >> output, "///////////////////////// Iterazione: ",i," /////////////////////////"
    
    beta = b
    step = 100
    #confidence = 0.1

    print >> output, "Beta: ", str(beta)
    print >> output, "Step massimi: ", str(step)
    print >> output, "Confidence: ", str(confidence)
    
    start_time = timeit.default_timer()
    steps,  ranks = topicSensitivePageRank(graph, beta, step,confidence)
    topic_sensitive_page_rank_elapsed = timeit.default_timer() - start_time
    
    print >> output, "Step utilizzati: ", str(steps)
    #for doc in ranks:
    	#print >> output, "Ranks: ", doc, "--->", ranks[doc]
    print >> output, "Tempo impiegato: ", str(topic_sensitive_page_rank_elapsed)
    
    return ranks
    
"""This method draws out the 20 documents of the basic match  from the basic page rank graph (sorting them in descending order)"""
def combine_basic_match_page_rank(basic_best_docs, page_ranks, output, i):
    print >> output, "///////////////////////// Combining Basic Best Match and Page Rank /////////////////////////"
    print >> output, "///////////////////////// Iterazione: ",i," /////////////////////////"

    start_time = timeit.default_timer()
    
    tmp = dict()
    for doc in basic_best_docs:
        for doc2 in page_ranks:
            if doc==doc2:
            		if doc not in tmp:
                		tmp[doc] = 0
            		tmp[doc] = page_ranks[doc]
		

    temp =  sorted(tmp, key=lambda x: tmp[x], reverse=True)
    sorted_docs = od((x, tmp[x]) for x in temp)
    
    combine_basic_match_page_rank_elapsed = timeit.default_timer() - start_time

    print >> output, "Tempo impiegato: ", str(combine_basic_match_page_rank_elapsed)

    print >> output, "Migliori 20 documenti con relativo page rank: "
    for doc in sorted_docs:
        print >> output, doc, str(sorted_docs[doc])
        
    
"""This method draws out the 20 documents of the optimized match  from the basic page rank graph (sorting them in descending order)"""
def combine_opt_match_page_rank(opt_best_docs,  page_ranks, output, i):
    print >> output, "///////////////////////// Combining Opt Best Match and Page Rank /////////////////////////"
    print >> output, "///////////////////////// Iterazione: ",i," /////////////////////////"

    start_time = timeit.default_timer()
    
    tmp = dict()
    for doc in opt_best_docs:
        for doc2 in page_ranks:
            if doc==doc2:
            		if doc not in tmp:
                		tmp[doc] = 0
            		tmp[doc] = page_ranks[doc]
		

    temp =  sorted(tmp, key=lambda x: tmp[x], reverse=True)
    sorted_docs = od((x, tmp[x]) for x in temp)
    combine_opt_match_page_rank_elapsed = timeit.default_timer() - start_time
    print >> output, "Tempo impiegato: ", str(combine_opt_match_page_rank_elapsed)

    print >> output, "Migliori 20 documenti con relativo page rank"
    for doc in sorted_docs:
        print >> output, doc, str(sorted_docs[doc])        
    
"""This method draws out the 20 documents of the basic match  from the topic sensitive page rank graph (sorting them in descending order)"""
def combine_basic_match_topic_sensitive_page_rank(basic_best_docs,  ts_page_ranks, output, i):
    print >> output, "///////////////////////// Combining Basic Best Match and Topic Sensitive Page Rank /////////////////////////"
    print >> output, "///////////////////////// Iterazione: ",i," /////////////////////////"

    start_time = timeit.default_timer()

    temp1 =  sorted(ts_page_ranks, key=lambda x: ts_page_ranks[x], reverse=True)
    ts_pr = od((x, ts_page_ranks[x]) for x in temp1)

    tmp = dict()
    for doc in basic_best_docs:
        for topic in ts_pr.keys():
            for doc2 in ts_pr[topic]:
                if doc==doc2:
                    if doc not in tmp:
                    	tmp[doc] = 0
                    tmp[doc] = ts_pr[topic][doc]
				
          
    temp =  sorted(tmp, key=lambda x: tmp[x], reverse=True)
    sorted_docs = od((x, tmp[x]) for x in temp)
    
    
    combine_basic_match_topic_sensitive_page_rank = timeit.default_timer() - start_time
    print >> output, "Tempo impiegato: ", str(combine_basic_match_topic_sensitive_page_rank)

    print >> output, "Migliori 20 documenti con relativo topic sensitive page rank: "
    print >> output, sorted_docs
    
"""This method draws out the 20 documents of the optimized match  from the topic sensitive page rank graph (sorting them in descending order)"""
def combine_opt_match_topic_sensitive_page_rank(opt_best_docs,  ts_page_ranks, output, i):
    print >> output, "///////////////////////// Combining Opt Best Match and Topic Sensitive Page Rank /////////////////////////"
    print >> output, "///////////////////////// Iterazione: ",i," /////////////////////////"

    start_time = timeit.default_timer()

    tmp = dict()
    for doc in opt_best_docs:
        for topic in ts_page_ranks.keys():
            for doc2 in ts_page_ranks[topic]:
                if doc==doc2:
                    if doc not in tmp:
                        tmp[doc] = 0
                    tmp[doc] = ts_page_ranks[topic][doc]

            
    temp =  sorted(tmp, key=lambda x: tmp[x], reverse=True)
    sorted_docs = od((x, tmp[x]) for x in temp)
    
    combine_opt_match_topic_sensitive_page_rank = timeit.default_timer() - start_time
    print >> output, "Tempo impiegato: ", str(combine_opt_match_topic_sensitive_page_rank)

    print >> output, "Migliori 20 documenti con relativo topic sensitive page rank: "
    print >> output, sorted_docs



#Best Match control flags
RUN_BBM = False
RUN_OBM = False

#Page rank control flags
RUN_PR = False
RUN_TSPR = False

#Combine control flags
COM_BBM_PR = False
COM_OBM_PR = False
COM_BBM_TSPR = False
COM_OBM_TSPR = False

#Reading input parameters
arguments = iter(sys.argv)

#skip the first: name of the script
next(arguments)

nomeDir="result"

#Switching input flags
for arg in arguments:
    nomeDir=nomeDir+"_"+arg
    if arg=="bbm":
        RUN_BBM = True
    elif arg=="obm":
        RUN_OBM=True
    elif arg=="pr":
        RUN_PR = True
    elif arg == "tspr":
        RUN_TSPR = True
    elif arg=="c1":
        COM_BBM_PR=True
    elif arg=="c2":    
        COM_OBM_PR=True
    elif arg=="c3":
        COM_BBM_TSPR=True
    elif arg=="c4":
        COM_OBM_TSPR=True
    else:
        raise IOError("error passing arguments")

starting_beta = 0.8

if not os.path.exists(os.getcwd()+"/"+nomeDir):
	os.makedirs(os.getcwd()+"/"+nomeDir)
else:
        raise IOError("folder already exists")

print ("///////////////////////// Reading Input Files /////////////////////////")

graph = readGraph()
if RUN_OBM:
    inverted_db = readInvertedDB()

if RUN_BBM:
    basic_best_docs = run_basic_best_match()
    
if RUN_OBM:
    opt_best_docs = run_opt_best_match(inverted_db)
    
if RUN_PR:	
    confidence=0
    for j in range(3):
        curr_beta = starting_beta
        if not os.path.exists(os.getcwd()+"/"+nomeDir+"/"+"confidence_"+str(confidence)):
            os.makedirs(os.getcwd()+"/"+nomeDir+"/"+"confidence_"+str(confidence))
        for i in range(2):
            output = open(os.getcwd()+"/"+nomeDir+"/"+"confidence_"+str(confidence)+"/"+str(curr_beta)+"_classic.txt", "w")
            page_ranks = run_page_rank(graph,output,curr_beta,i,confidence)
            if COM_BBM_PR:
        	    combine_basic_match_page_rank(basic_best_docs, page_ranks,output,i)
            if COM_OBM_PR:
        	    combine_opt_match_page_rank(opt_best_docs, page_ranks,output,i)
            curr_beta+=0.05
        confidence = confidence + 0.000001
    print ("///////////////Page Rank finished////////////////")

if RUN_TSPR:
    confidence=0
    for j in range(3):
        curr_beta = starting_beta
        if not os.path.exists(os.getcwd()+"/"+nomeDir+"/"+"confidence_"+str(confidence)):
            os.makedirs(os.getcwd()+"/"+nomeDir+"/"+"confidence_"+str(confidence))
        for i in range(2):
            output = open(os.getcwd()+"/"+nomeDir+"/"+"confidence_"+str(confidence)+"/"+str(curr_beta)+"_ts.txt", "w")
            ts_page_ranks = run_topic_sensitive_page_rank(graph,output,curr_beta,i,confidence)
            if COM_BBM_TSPR:
                combine_basic_match_topic_sensitive_page_rank(basic_best_docs, ts_page_ranks,output,i)
            if COM_OBM_TSPR:
                combine_opt_match_topic_sensitive_page_rank(opt_best_docs, ts_page_ranks,output,i)
            curr_beta+=0.05
        confidence = confidence + 0.000001
    print ("////////////TS Page Rank finished///////////////")

print ("///////////////////////// Testing Finished /////////////////////////")

    
