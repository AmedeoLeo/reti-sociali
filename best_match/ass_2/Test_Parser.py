#!/usr/bin/python

from Impl_Parser import read_wibbi
from HTMLParser import HTMLParser
#from re import findall, sub
import re
import sys
import os
reload(sys)

tag = True
parser = HTMLParser()
sys.setdefaultencoding('UTF8')
output = open("output.txt", "w")
topic = "sport"

for filename in os.listdir(os.getcwd()):
    if filename.endswith(".pages"):
        #topic = "test"
        graph,db = read_wibbi("./"+filename, topic)
        #graph,db = read_wibbi("./"+filename)
        for topic in graph.keys():
            toPrint = topic
            for i in graph[topic].keys():
                toPrint += i+ "["
                for val in db[topic][i]:
                    if '<' in val:
                        tag = False
                    elif '/>' in val:
                        tag = True
                    elif re.match("^[A-Za-z0-9]*$", val):
                        html_decoded_string = parser.unescape(val)
                        toPrint += html_decoded_string + ","
                print >> output,  toPrint + "]"    
            print >> output, "--------------------------------------------------------------------------------"
output.close()
