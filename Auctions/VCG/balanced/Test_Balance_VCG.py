#!/usr/bin/python

from random import randint, random
from Impl_Balance_VCG import *

#All possible queries
queries=["prova","test","esempio"]
#queries=["test"]
#For each query, lists the available slots and their clickthrough rate
slot_ctrs=dict()

slot_ctrs["prova"]=dict()
slot_ctrs["prova"]["id1"] = 4
slot_ctrs["prova"]["id2"] = 3

slot_ctrs["test"]=dict()
slot_ctrs["test"]["id1"] = 5
slot_ctrs["test"]["id2"] = 4
slot_ctrs["test"]["id3"] = 3

slot_ctrs["esempio"]=dict()
slot_ctrs["esempio"]["id1"] = 3
slot_ctrs["esempio"]["id2"] = 4
"""
slot_ctrs["test"]=dict()
slot_ctrs["test"]["id1"] = 10
slot_ctrs["test"]["id2"] = 5
slot_ctrs["test"]["id3"] = 2
"""
#For each query, lists the advertisers that have a bid for that query and the value of this bid

adv_bids=dict()

adv_bids["prova"]=dict()
adv_bids["prova"]["x"] = 5
adv_bids["prova"]["y"] = 10

adv_bids["test"]=dict()
adv_bids["test"]["x"] = 4
adv_bids["test"]["y"] = 2

adv_bids["esempio"]=dict()
adv_bids["esempio"]["x"] = 6
adv_bids["esempio"]["z"] = 5

"""
adv_bids["test"]=dict()
adv_bids["test"]["x"] = 3
adv_bids["test"]["y"] = 2
adv_bids["test"]["z"] = 1
"""
#The initial budget of each advertisers
adv_budgets=dict()
adv_budgets["x"] = 10
adv_budgets["y"] = 5
adv_budgets["z"] =15

#It denotes the lenght of the sequence of queries that we will consider
num_query=5

#Generate a random sequence of num_query queries, with each query selected from the list queries
query_sequence=[]
for i in range(num_query):
    query_sequence.append(queries[randint(0,len(queries)-1)])
                          
print(query_sequence)
print "\n"

adv_cbudgets=adv_budgets.copy() #The current budgets of advertisers
revenue=0 #The current revenue of the auctioneer

for i in range(num_query):
    #For each query we use the balance algorithm for evaluating the assignment and the payments
    query_winners, query_pay = balance(slot_ctrs, adv_bids, adv_budgets, adv_cbudgets, query_sequence[i])
    
    for j in query_winners.keys():
        #We now simulate an user clicking on the ad with a probability that is equivalent to the slot's clickthrough rate
        p = random() # A number chosen uniformly at random between 0 and 1
        if p < slot_ctrs[query_sequence[i]][j]: #This event occurrs with probability that is exactly slot_ctrs[query_sequence[i]][j]
            print "Si e' verificato l'evento P per ", query_winners[j]
            adv_cbudgets[query_winners[j]] -= query_pay[query_winners[j]]
            revenue += query_pay[query_winners[j]]
            print "\n"
        else:
            "Non si e' verificato l'evento P, nessuno paga"
    print(query_winners, adv_cbudgets)
    print "\n"
    
print(revenue)
