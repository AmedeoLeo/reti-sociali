#!/usr/bin/python
from Impl_Parser import read_wibbi
from Impl_Matching import *
import sys
import timeit

query_terms=["obama", "picasso",  "chair", "champions league"]
reload(sys)
sys.setdefaultencoding('UTF8')

start_time = timeit.default_timer()
best_docs = best_match(query_terms,0)
elapsed_time = timeit.default_timer()-start_time
print elapsed_time
