from __future__ import division
from random import randint,  choice,  uniform
import sys
from VCG_bot.balanced.Impl_best_response_VCG import best_response
from VCG_bot.budget_saving.Impl_budg_saving_VCG import vcg
from FP_bot.FP_budget_saving.Impl_budg_saving_FP import  budget_saving_bot,  balance
from FP_bot.FP_competitor_bursting.Impl_comp_burst_FP import  competitor_bursting_bot
from FP_bot.FP_random.Impl_random_FP import  random_bot

from FP_best_response_bot.FP_altruistic.Impl_altruistic_FP import altruistic_best_response
from FP_best_response_bot.FP_competitor_bursting.Impl_competitor_bursting_FP import comp_burst_best_response



def find_better_strategy(adv_value,  adv_cbudg,  adv_sbudg,  viewed_query,  total_query):
    choice = 0
    strategy=""
    crazy_bidder = uniform(0, 1)
   
    #Case 1: I have a small consideration of that item and I don't want bid so much even if the auction is almost finished
    if adv_value >= 1 and adv_value <= 3:
       choice += 0.1
    
    #Case2: I have a medium consideration of that item but  I wouldn't submit a high bid if the auction is on first steps  
    elif (adv_value >= 4 and adv_value <= 7) and (viewed_query < int(total_query/2)):
        
        #Subcase1: I would bid higher if my current budget is high enough (higher than half of the starting budget)
        if adv_cbudg >  int(adv_sbudg/2):
            choice += 0.4
        #Subcase2: I wouldn't bid higher because my current budget is not high enough)
        else:
            choice += 0.2
            
    #Case3:  have a medium consideration of that item and I would submit a high bid if the auction is on last steps 
    elif (adv_value >= 4 and adv_value <= 7) and (viewed_query >= int(total_query/2)):
        #Subcase1: I would bid higher if my current budget is high enough (higher than half of the starting budget)
        if adv_cbudg >  int(adv_sbudg/2):
            choice += 0.6
        #Subcase2: I wouldn't bid higher because my current budget is not high enough)
        else:
            choice += 0.5
            
    #Case4: I want that item not matter if I have to go all in
    else:
        choice += 1

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

#All the slots 
all_slots = ["id1",  "id2",  "id3", "id4", "id5"]
#All the queries
#all_queries=["query1",  "query2", "query3","query4",  "query5", "query6","query7",  "query8", "query9", "query10"]
all_queries = ["query1"]
#All the advertisers
all_advertisers = ["adv1", "adv2", "adv3", "adv4", "adv5", "adv6","adv7"]
#all_advertisers = ["adv1","adv2"]

iterations = 10
    
"""
print (slot_ctrs)
print (adv_bids)
print (adv_sbudget)
"""
max_step=100

if format == "fp":
    print ("//////////Execute the  FIRST PRICE auction /////////")
elif format =="vcg":
    print ("//////////Execute the  VCG auction /////////")
else:
    raise IOError("error passing argument")

revenue_dict = []

auction_utility = []
auction_revenue = []

"""
 #Slots' clickthrough rates
slot_ctrs=dict()
slot_ctrs["query1"] = dict()
slot_ctrs["query1"]["id1"] = 6
slot_ctrs["query1"]["id2"] = 5
slot_ctrs["query1"]["id3"] = 4



#Advertisers' values
adv_values=dict()
adv_values["query1"] = dict()
adv_values["query1"]["x"] = 5
adv_values["query1"]["y"] = 4
adv_values["query1"]["z"] = 5
"""

for iter in range(0, iterations):
    
    print ("****************** RUN ", str(iter), "******************")
    
   
    """
    #budgets
    adv_sbudg = dict()
    adv_sbudg["x"] = 150
    adv_sbudg["y"] = 100
    adv_sbudg["z"] = 60
    """
    adv_sbudget = dict()
    slot_ctrs = dict()
    adv_values = dict()
    adv_bids = dict()
    adv_utility = dict()
    
    #for each query, inizialize all the data structures (click-through rate, values)
    
    for q in all_queries:
        if q not in slot_ctrs:
            #num_slots = randint(1, len(all_slots))
            num_slots = 3
            index = 0
            slot_ctrs[q] = dict()
            while index < num_slots:
               current_slot = choice(all_slots)
               if current_slot not in slot_ctrs[q]:
                   slot_ctrs[q][current_slot] = randint(1, 50)
                   index+=1
        if q not in adv_values:
            #num_adv = randint(1, len(all_advertisers))
            num_adv = 3

            adv_values[q] = dict()
            index = 0
            while index < num_adv:
               current_adv = choice(all_advertisers)
               if current_adv not in adv_values[q]:
                   adv_values[q][current_adv] = randint(1, 100)
                   index+=1
    #randomly inizialize the starting budget for each adverstiser
    for adv in all_advertisers:
        adv_sbudget[adv] = randint(20, 60) 
    
    done = False
    step = 0
    viewed_query = 0
    adv_cbudg = adv_sbudget
    history=[]
    adv_bids = dict()
    adv_utility = dict()
    adv_revenue = dict()
    
    while not done and step < max_step:
        done = True
        for query in adv_values.keys():
            viewed_query +=1
            if query not in adv_bids:
                adv_bids[query] = dict()
            for i in adv_values[query].keys():
                #strategy = find_better_strategy(adv_values[query][i], adv_cbudg[i],  adv_sbudget[i], viewed_query,  len(adv_values.keys()))
                strategy = "altruistic"
                #print ("****************** ADV ", i, " IS PLAYING A ",strategy," STRATEGY ******************")

                   
                if strategy == "altruistic":
                    adv_bids[query][i] = altruistic_best_response(i,adv_values[query][i],slot_ctrs[query],history, query, step)
            
                 
                elif strategy =="comp_burst":   
                    adv_bids[query][i] = comp_burst_best_response(i,adv_values[query][i],slot_ctrs[query],history, query, step)
                
                elif strategy =="random":   
                    adv_bids[query][i] = random_bot(i,adv_values[query][i],slot_ctrs[query],history, query, step)
                
                
                if step == 0 or adv_bids[query][i] != history[step-1][query]["adv_bids"][i]:
                    done=False
                    
                    if step!=0:
                        if query not in  history[step-1]:
                            continue

             
                        
            if done:
                break
                        
            if format == "fp":
                adv_slots, adv_pays = balance(slot_ctrs[query],adv_bids[query], adv_cbudg, adv_sbudget)
            elif format =="vcg":
                adv_slots, adv_pays = vcg(slot_ctrs[query],adv_bids[query])
            
        
            #Update budget
            done = True
            for adv in adv_pays:
                #se ogni bidder non ha piu budget mi fermo
                if adv_pays[adv] <  adv_cbudg[adv]:
                    if adv not in adv_utility:
                        adv_utility[adv] = 0
                    if adv not in adv_revenue:
                        adv_revenue[adv] = 0

                    adv_utility[adv] = adv_values[query][adv] - adv_pays[adv]
                    adv_revenue[adv] =   adv_pays[adv]
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
             
        #print(step, history[step])
        print ("\n")
        step += 1
    
    tot_utility = 0
    tot_revenue = 0
    for adv in adv_utility:
        tot_utility+=adv_utility[adv]
    auction_utility.append(tot_utility)
    for adv in adv_revenue:
        tot_revenue+=adv_revenue[adv]
    auction_revenue.append(tot_revenue)


temp1 =0
temp2=0
output =open("balanced.txt", "w")
   
denom_rv =0
denom_ut=0
 
 

        
for ut in auction_utility:
    temp1+=ut
for rv in auction_revenue:
    temp2+=rv
    
print >> output, "media utilita (con l'accento): ", temp1/iterations
print >> output, "media revenue: ", temp2/iterations


output.close()












