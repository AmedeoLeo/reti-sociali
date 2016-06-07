import timeit
import sys
from Impl_Topic_Sensitive_PageRank import readGraph,  topicSensitivePageRank
from Impl_Opt_Matching import readInvertedDB,  opt_best_match
from Impl_Basic_Matching import basic_best_match, readCountDB
from Impl_PageRank import pageRank2


def run_basic_best_match():
    print ("///////////////////////// Running Basic Best Match /////////////////////////")
    
    query="obama,champions league"
    threshold=0
    
    start_time = timeit.default_timer()
    basic_best_docs = basic_best_match(query,threshold)
    basic_match_elapsed = timeit.default_timer() - start_time
    print (basic_best_docs)
    print (basic_match_elapsed)
    
    return basic_best_docs
    
    
def run_opt_best_match(inverted_db):
    print ("///////////////////////// Running Opt Best Match /////////////////////////")
    
    query="the winner of uefa champions leaugue"
    threshold=0
    
    start_time = timeit.default_timer()
    opt_best_docs = opt_best_match(inverted_db, query,threshold)
    opt_match_elapsed = timeit.default_timer() - start_time
    
    print (opt_best_docs)
    print (opt_match_elapsed)
    return opt_best_docs

def run_page_rank(graph):
    print ("///////////////////////// Running Page Rank /////////////////////////")
    
    beta = 0.85
    step = 100
    confidence = 1
    
    start_time = timeit.default_timer()
    steps,  ranks = pageRank2(graph, beta, step,confidence)
    page_rank_elapsed = timeit.default_timer() - start_time
    
    print (page_rank_elapsed)
    return steps, ranks

def run_topic_sensitive_page_rank(graph):
    print ("///////////////////////// Running Topic Sensitive Page Rank /////////////////////////")
    
    beta = 0.85
    step = 100
    confidence = 1
    
    start_time = timeit.default_timer()
    steps,  ranks = topicSensitivePageRank(graph, beta, step,confidence)
    topic_sensitive_page_rank_elapsed = timeit.default_timer() - start_time
    
    print (topic_sensitive_page_rank_elapsed)
    return steps,  ranks
    
def combine_basic_match_page_rank(basic_best_docs, page_ranks):
    print ("///////////////////////// Combining Basic Best Match and Page Rank /////////////////////////")
    tmp = dict()
    for doc in basic_best_docs:
        if doc in page_ranks.keys():
            if doc not in tmp:
                tmp[doc] = 0
            tmp[doc] = page_ranks[doc]
    
    print (tmp)
    

def combine_opt_match_page_rank(opt_best_docs,  page_ranks):
    print ("///////////////////////// Combining Opt Best Match and Page Rank /////////////////////////")
    tmp = dict()
    for doc in opt_best_docs:
        if doc in page_ranks.keys():
            if doc not in tmp:
                tmp[doc] = 0
            tmp[doc] = page_ranks[doc]
    print (tmp)
    
def combine_basic_match_topic_sensitive_page_rank(basic_best_docs,  ts_page_ranks):
    print ("///////////////////////// Combining Basic Best Match and Topic Sensitive Page Rank /////////////////////////")
    tmp = dict()
    for doc in basic_best_docs:
        for topic in ts_page_ranks.keys():
            if doc in ts_page_ranks[topic]:
                if doc not in tmp:
                    tmp[doc] = 0
            tmp[doc] = ts_page_ranks[topic][doc]
    print (tmp)
    
    
def combine_opt_match_topic_sensitive_page_rank(opt_best_docs,  ts_page_ranks):
    print ("///////////////////////// Combining Opt Best Match and Topic Sensitive Page Rank /////////////////////////")
    tmp = dict()
    for doc in opt_best_docs:
        for topic in ts_page_ranks.keys():
            if doc in ts_page_ranks[topic]:
                if doc not in tmp:
                    tmp[doc] = 0
            tmp[doc] = ts_page_ranks[topic][doc]
    print (tmp)


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

#Switching input flags
for arg in arguments:
    print (arg)
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

        
print ("///////////////////////// Reading Input Files /////////////////////////")

graph = readGraph()
if RUN_OBM:
    inverted_db = readInvertedDB()




if RUN_BBM:
    basic_best_docs = run_basic_best_match()
if RUN_OBM:
    opt_best_docs = run_opt_best_match(inverted_db)
if RUN_PR:
    page_ranks = run_page_rank(graph)
if RUN_TSPR:
    ts_page_ranks = run_topic_sensitive_page_rank(graph)
if COM_BBM_PR:
    combine_basic_match_page_rank(basic_best_docs, page_ranks)
if COM_OBM_PR:
    combine_opt_match_page_rank(opt_best_docs,  page_ranks)
if COM_BBM_TSPR:
    combine_basic_match_topic_sensitive_page_rank(basic_best_docs,  ts_page_ranks)
if COM_OBM_TSPR:
    combine_opt_match_topic_sensitive_page_rank(opt_best_docs,  ts_page_ranks)


print ("///////////////////////// Testing Finished /////////////////////////")


    
