#!/usr/bin/python

from Parser import read_wibbi
import os
import random

"""This method prints on file the parsed graph"""
def print_graph(dataset):
    output = open("graph.txt","w")
    toPrint = ""
    for topic in dataset.keys():
        toPrint = topic+" "
        for url in dataset[topic].keys():
            toPrint+= url+";"
            for neighbor in dataset[topic][url]:
                toPrint+=neighbor+","
            toPrint+="*"
        print >> output,  toPrint
        
    output.close()
    

def set_default(obj):
	if isinstance(obj,set):
		return list(obj)
	raise TypeError

"""This method randomly generates ten links between the pages"""
def create_link(dataset):
  for name1 in dataset:
      for name2 in dataset:
         if name1!=name2:

             U = random.sample(dataset[name1].keys(),10)
             V = random.sample(dataset[name2].keys(),10)

             for i in range(len(U)):
                 if V[i] not in dataset[name1][U[i]]: 
                     dataset[name1][U[i]].add(V[i])




dataset = dict()
print("------STARTING TO PARSE-----")

for filename in os.listdir(os.getcwd()+"/dataset/"):
    
    if filename.endswith(".pages"):
        print("Parsing: " + filename)
        topic = filename.split("_")[0]
        graph = read_wibbi(filename)
        dataset[topic] = graph
        print("----------------")


print("------FINISHED PARSING-----")

print ("------STARTING CONNECT----------")

create_link(dataset)
print("-------PRINTING GRAPH-------------")

    
print_graph(dataset)

print("------DONE-----")





