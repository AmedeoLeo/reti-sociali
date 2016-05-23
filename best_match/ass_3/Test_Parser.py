#!/usr/bin/python
from Impl_Parser import read_wibbi
from HTMLParser import HTMLParser
from Impl_Matching import best_match
import sys
#from re import findall, sub

query_terms=["state", "staff",  "state staff"]
reload(sys)
K = 60
tag = True
parser = HTMLParser()
sys.setdefaultencoding('UTF8')
output = open("output.txt", "w")

#topic = "test"
graph,sorted_db,  count_db = read_wibbi()

best_docs = best_match(query_terms,  0,  sorted_db, count_db)


for elem in sorted_db:
    print >> output,  elem
    print >> output,  len(sorted_db[elem])
    print >> output, sorted_db[elem]


output.close()
