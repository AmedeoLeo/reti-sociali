from __future__ import division
from random import randint,  choice,  uniform
import sys
import timeit

#importing auction formats
from impl_auction_formats import vcg,  balanced_FP
#importing bots
from bots.Impl_balanced_best_response import balanced_best_response
from bots.Impl_budget_saving import budget_saving_bot
from bots.Impl_comp_burst import competitor_bursting_bot
from bots.Impl_random import random_bot
from bots.Impl_altruistic_best_response import altruistic_best_response
from bots.Impl_competitor_bursting_best_response import comp_burst_best_response

"""
    This method simulates an auction game where each player decides the best strategy considering three factors:
        1. State of the auction
        2. Remaining budget
        3. Evaluation for the item
"""
def find_best_strategy(adv_value,  adv_cbudg,  adv_sbudg,  viewed_query,  total_query):
    choice = 0
    strategy=""
    crazy_bidder = uniform(0, 1)
    
    tot_value = 0
    for val in adv_value:
        tot_value += adv_value[val]
    avg_value = tot_value/len(adv_value)
    
    #Case 1: I have a small consideration of that item and I don't want bid so much even if the auction is almost finished
    if avg_value >= 1 and avg_value <= 3:
       choice += 0.1
    
    #Case2: I have a medium consideration of that item but  I wouldn't submit a high bid if the auction is on first steps  
    if (avg_value >= 4 and avg_value <= 7) and (viewed_query < int(total_query/2)):
        
        #Subcase1: I would bid higher if my current budget is high enough (higher than half of the starting budget)
        if adv_cbudg >  int(adv_sbudg/2):
            choice += 0.4
        #Subcase2: I wouldn't bid higher because my current budget is not high enough)
        else:
            choice += 0.2
            
    #Case3:  have a medium consideration of that item and I would submit a high bid if the auction is on last steps 
    if (avg_value >= 4 and avg_value <= 7) and (viewed_query >= int(total_query/2)):
        #Subcase1: I would bid higher if my current budget is high enough (higher than half of the starting budget)
        if adv_cbudg >  int(adv_sbudg/2):
            choice += 0.6
        #Subcase2: I wouldn't bid higher because my current budget is not high enough)
        else:
            choice += 0.5
            
    #Case4: I want that item not matter if I have to go all in
    if avg_value >= 7:
        choice += 1
    
    #Madness factor: we also consider people which don't follow any strategy (we call them crazy bidder)
    #those crazy bidders will follow the random strategy with a (small) probability
    if crazy_bidder <= 0.05:
        strategy = "random"
    elif choice >= 1:
        strategy = "comp_burst"
    else:
        strategy = "altruistic"
    
    return strategy


#Reading input parameters
arguments = iter(sys.argv)
#skip the first: name of the script
next(arguments)
format = next(arguments)
bot = next(arguments,None)

#All the slots 
all_slots = ["id1", "id2",  "id3"]

#All the queries
all_queries=["query1",  "query2", "query3","query4",  "query5", "query6","query7",  "query8", "query9", "query10"]
#all_queries = ["query1", "query2"]

#All the advertisers
#all_advertisers = ["adv1", "adv2", "adv3", "adv4", "adv5", "adv6","adv7"]
all_advertisers = ["adv1","adv2","adv3"]

iterations = 500
max_step=100

tot_step =0
tot_time=0
if format == "fp":
    print ("//////////Execute the  FIRST PRICE auction /////////")
elif format =="vcg":
    print ("//////////Execute the  VCG auction /////////")
else:
    raise IOError("error passing format argument")


#Fixed values
"""
 #Slots' clickthrough rates
slot_ctrs=dict()
slot_ctrs["query1"] = dict()
slot_ctrs["query1"]["id1"] = 6
slot_ctrs["query1"]["id2"] = 5
slot_ctrs["query1"]["id3"] = 4

slot_ctrs["query2"] = dict()
slot_ctrs["query2"]["id1"] = 4
slot_ctrs["query2"]["id2"] = 2
slot_ctrs["query2"]["id3"] = 1


#Advertisers' values
adv_values=dict()
adv_values["query1"] = dict()
adv_values["query1"]["adv1"] = dict()
adv_values["query1"]["adv1"]["id1"] = 5
adv_values["query1"]["adv1"]["id2"] = 4
adv_values["query1"]["adv1"]["id3"] = 3

adv_values["query1"]["adv2"] = dict()
adv_values["query1"]["adv2"]["id1"] = 7
adv_values["query1"]["adv2"]["id2"] = 3
adv_values["query1"]["adv2"]["id3"] = 2

adv_values["query1"]["adv3"] = dict()
adv_values["query1"]["adv3"]["id1"] = 3
adv_values["query1"]["adv3"]["id2"] = 2
adv_values["query1"]["adv3"]["id3"] = 1

adv_values["query2"] = dict()
adv_values["query2"]["adv1"] = dict()
adv_values["query2"]["adv1"]["id1"] = 8
adv_values["query2"]["adv1"]["id2"] = 5
adv_values["query2"]["adv1"]["id3"] = 2

adv_values["query2"]["adv2"] = dict()
adv_values["query2"]["adv2"]["id1"] = 5
adv_values["query2"]["adv2"]["id2"] = 2
adv_values["query2"]["adv2"]["id3"] = 1

adv_values["query2"]["adv3"] = dict()
adv_values["query2"]["adv3"]["id1"] = 10
adv_values["query2"]["adv3"]["id2"] = 9
adv_values["query2"]["adv3"]["id3"] = 16
"""


revenue_dict = []
auction_utility = []
auction_revenue = []
for iter in range(0, iterations):
    start_time = timeit.default_timer()
    print ("****************** RUN ", str(iter), "******************")

    adv_sbudg = dict()
    slot_ctrs = dict()
    adv_values = dict()
    adv_bids = dict()
    adv_utility = dict()
    
    done = False
    step = 0
    viewed_query = 0
    history=[]
    adv_revenue = dict()
        
    for q in all_queries:
        if q not in slot_ctrs:
            #we only consider a fixed number of slots for each run
            num_slots = 3
            index = 0
            slot_ctrs[q] = dict()
            while index < num_slots:
                current_slot = choice(all_slots)
                if current_slot not in slot_ctrs[q]:
                    slot_ctrs[q][current_slot] = randint(1, 10)
                    index+=1
        if q not in adv_values:
            #we only consider a fixed number of advertisers for each run
            num_adv = 3
            adv_values[q] = dict()
            index = 0
            while index < num_adv:
                current_adv = choice(all_advertisers)
                if current_adv not in adv_values[q]:
                    adv_values[q][current_adv] = dict()
                    index2=0
                    while index2 < num_slots:
                        current_slot = choice(all_slots)
                        if current_slot not in adv_values[q][current_adv]:
                            adv_values[q][current_adv][current_slot] = randint(1, 15)
                            index2+=1
                    index+=1
    #randomly inizialize the starting budget for each adverstiser
    for adv in all_advertisers:
        adv_sbudg[adv] = randint(20, 60) 
		    
    adv_bids = dict()
    adv_utility = dict()
 
    done = False
    step = 0
    viewed_query = 0
    history=[]
    adv_revenue = dict()
            
    """
    #budgets
    adv_sbudg = dict()
    adv_sbudg["adv1"] = 60
	adv_sbudg["adv2"] = 100
    adv_sbudg["adv3"] = 150
    """
            
    adv_cbudg = adv_sbudg
    while not done and step < max_step:
        done = True
        for query in adv_values.keys():
            if query not in adv_utility:
                adv_utility[query] = dict()
            if query not in adv_revenue:
                adv_revenue[query] = dict()
			
            viewed_query +=1
            if query not in adv_bids:
                adv_bids[query] = dict()
            for i in adv_values[query].keys():
                if bot == None:
                    #print ("////////////////////// RUNNING COMBINATION BOT ////////////////////////")
                    strategy = find_best_strategy(adv_values[query][i], adv_cbudg[i],  adv_sbudg[i], viewed_query,  len(adv_values.keys()))            
                else:
                    strategy = bot
                print  ("****************** ADV ", i, " IS PLAYING A ",strategy," STRATEGY ******************")
				
                if strategy == "balanced":
                    adv_bids[query][i] = balanced_best_response(i,adv_values[query][i],slot_ctrs[query],history,query,step)
                elif strategy =="budget_saving":   
                    adv_bids[query][i] = budget_saving_bot(i,adv_values[query][i],slot_ctrs[query],history, query, step)
                elif strategy =="comp_burst":   
                    adv_bids[query][i] = competitor_bursting_bot(i,adv_values[query][i],slot_ctrs[query],history, query, step)
                elif strategy =="comp_burst_br":   
                    adv_bids[query][i] = comp_burst_best_response(i,adv_values[query][i],slot_ctrs[query],history, query, step)
                elif strategy =="random":   
                    adv_bids[query][i] = random_bot(i,adv_values[query][i],slot_ctrs[query],history, query, step)
                elif strategy =="altruistic":   
                    adv_bids[query][i] = altruistic_best_response(i,adv_values[query][i],slot_ctrs[query],history, query, step)
                else:
                    raise IOError("error passing bot argument")
			
                if step == 0 or adv_bids[query][i] != history[step-1][query]["adv_bids"][i]:
                    done=False
				    
                    if step!=0:
                        if query not in  history[step-1]:
                            continue

			     
					
                if done:
                    break
					
            if format == "fp":
                adv_slots, adv_pays = balanced_FP(slot_ctrs[query],adv_bids[query], adv_cbudg, adv_sbudg)
            elif format =="vcg":
                adv_slots, adv_pays = vcg(slot_ctrs[query],adv_bids[query])
			    
			    
			#Update budget
            done = True

            for adv in adv_pays:
	            #If every adv runs out of his budget the auction must be stopped
                if adv_pays[adv] <  adv_cbudg[adv]:
                    if adv not in adv_utility[query]:
                        adv_utility[query][adv] = 0
                    if adv not in adv_revenue[query]:
                        adv_revenue[query][adv] = 0
                    if adv_slots[adv] in adv_values[query][adv]:
                        adv_utility[query][adv] +=slot_ctrs[query][adv_slots[adv]]*(adv_values[query][adv][adv_slots[adv]] - adv_pays[adv])
                        adv_revenue[query][adv] += slot_ctrs[query][adv_slots[adv]]*adv_pays[adv]
                        adv_cbudg[adv]-=adv_pays[adv]
                    done = False
	
            #Update the history
            history.append(dict())
            if query not in history[step]:
                history[step][query] = dict()
            history[step][query]["adv_bids"]=dict(adv_bids[query])
            history[step][query]["adv_slots"]=dict(adv_slots)
            history[step][query]["adv_pays"]=dict(adv_pays)
            history[step][query]["adv_cbudg"]=dict(adv_cbudg)

        step += 1



    tot_step+=step
    tot_utility = 0
    tot_revenue = 0
    for query in adv_utility:
        for adv in adv_utility[query]:
            tot_utility+=adv_utility[query][adv]
    auction_utility.append(tot_utility/step)
    for query in adv_revenue:
        for adv in adv_revenue[query]:
            tot_revenue+=adv_revenue[query][adv]
    auction_revenue.append(tot_revenue/step)
    elapsed_time = timeit.default_timer()-start_time
    tot_time+=elapsed_time
	
temp1=0
temp2=0
filename=""
if bot==None:
    filename=format+"_combination.txt"
else:
    filename=format+"_"+bot+".txt"
output = open(filename,"w")
	    
for ut in auction_utility:
	temp1+=ut
for rv in auction_revenue:
	temp2+=rv
print >> output, "media utilita: ", temp1/iterations
print >> output, "media revenue: ", temp2/iterations
print >> output, "media step: ", tot_step/iterations
print >> output, "media tempo: ", tot_time/iterations
print >> output, "-------------------------------------------------------"
output.close()
