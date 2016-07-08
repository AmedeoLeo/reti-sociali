#!/usr/bin/python

from Parser import read_wibbi
import os

""""This method print on file the inverted_db"""
def printInvertedDB(inverted_db, output):
    
    toPrint = ""
    for term in inverted_db.keys():
        toPrint = term + " "
        for doc in inverted_db[term]:
            toPrint += doc + ","
            toPrint+=str(inverted_db[term][doc])+";"
        print >> output, toPrint

"""This method print on file the count_db"""
def printCountDB(count_db, output):
    toPrint = ""
    for doc in count_db.keys():
        toPrint = doc + " "
        for term in count_db[doc]:
            toPrint += term + ","
        print >> output, toPrint
    
"""This method performs the db reversal"""    
def invert(db):
    inverted_db = dict()
    for url in db.keys():
        size = len(db[url])
        for word in db[url]:
            if word not in inverted_db.keys():
                inverted_db[word] = dict()
            count = db[url].count(word)
            inverted_db[word][url] = float(count)/ size
    return inverted_db

def set_default(obj):
	if isinstance(obj,set):
		return list(obj)
	raise TypeError


dataset = dict()
for filename in os.listdir(os.getcwd()+"/dataset/"):
    
    if filename.endswith(".pages"):
        print("Parsing: " + filename)
        graph,db = read_wibbi(filename)
        dataset[filename] = db
        print("----------------")
print("------FINISHED PARSING-----")

print("------PRINTING COUNT DB-----")
output = open("count_db.txt","w")
for filename in dataset.keys():
    print("-------WRITING "+filename+ "-------------")
    printCountDB(dataset[filename], output)

output.close()
print("------DONE-----")


print ("------STARTING INVERSE----------")
output = open("inverted_db.txt","w")
for filename in dataset.keys():
    print("-------INVERTING "+filename+ "-------------")
    printInvertedDB(invert(dataset[filename]), output)
output.close()

print("------DONE-----")
