#!/usr/bin/python
from Impl_Parser import read_wibbi
from HTMLParser import HTMLParser
from Impl_Matching import *
import sys
#from re import findall, sub

query_terms=["obama", "picasso",  "chair", "champions league"]
reload(sys)
tag = True
parser = HTMLParser()
sys.setdefaultencoding('UTF8')

#graph,sorted_db,count_db = read_wibbi()
count_db = read_wibbi()
best_docs = best_match(query_terms,0,count_db)

