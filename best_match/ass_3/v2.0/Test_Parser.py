#!/usr/bin/python
from Impl_Parser import read_wibbi
import timeit
#from Parser import read_wibbi
import sys
#from re import findall, sub
reload(sys)

sys.setdefaultencoding('UTF8')
start_time = timeit.default_timer()

read_wibbi()
elapsed_time = timeit.default_timer()-start_time
print elapsed_time
