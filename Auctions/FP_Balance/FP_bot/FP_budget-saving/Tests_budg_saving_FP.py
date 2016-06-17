#!/usr/bin/python

from Impl_budg_saving_FP import balance,  budget_saving_bot

#queries
queries = ["test", "prova", "esame"]


#Slots' clickthrough rates
slot_ctrs=dict()
slot_ctrs["test"] = dict()
slot_ctrs["test"]["id1"] = 10
slot_ctrs["test"]["id2"] = 5
slot_ctrs["test"]["id3"] = 2

slot_ctrs["prova"] = dict()
slot_ctrs["prova"]["id1"] = 8
slot_ctrs["prova"]["id2"] = 7
slot_ctrs["prova"]["id3"] = 4

slot_ctrs["esame"] = dict()
slot_ctrs["esame"]["id1"] = 5
slot_ctrs["esame"]["id2"] = 2
slot_ctrs["esame"]["id3"] = 1

#Advertisers' values
adv_values=dict()
adv_values["test"] = dict()
adv_values["test"]["x"] = 5
adv_values["test"]["y"] = 4
adv_values["test"]["z"] = 2

adv_values["prova"] = dict()
adv_values["prova"]["x"] = 3
adv_values["prova"]["y"] = 2
adv_values["prova"]["z"] = 1

adv_values["esame"] = dict()
adv_values["esame"]["x"] = 2
adv_values["esame"]["y"] = 1
adv_values["esame"]["z"] = 0


#Advertisers' bots
adv_bots=dict()
adv_bots["test"] = dict()
adv_bots["test"]["x"] = budget_saving_bot
adv_bots["test"]["y"] = budget_saving_bot
adv_bots["test"]["z"] = budget_saving_bot

adv_bots["prova"] = dict()
adv_bots["prova"]["x"] = budget_saving_bot
adv_bots["prova"]["y"] = budget_saving_bot
adv_bots["prova"]["z"] = budget_saving_bot

adv_bots["esame"] = dict()
adv_bots["esame"]["x"] = budget_saving_bot
adv_bots["esame"]["y"] = budget_saving_bot
adv_bots["esame"]["z"] = budget_saving_bot

#budgets
adv_sbudg = dict()
adv_sbudg["x"] = 150
adv_sbudg["y"] = 100
adv_sbudg["z"] = 60


step=0
history=[]
adv_bids=dict()
adv_cbudg = adv_sbudg

done=False
max_step=100

#We repeat the auctions as long as an equilibrium has not been reached.
#(This mean that advertisers submit the same bids in any successive repetition.)
#If an equilibrium is not reached in short time, then we stop after max_step steps
while not done and step < max_step:
        done = True
        for query in adv_values.keys():
            if query not in adv_bids:
                adv_bids[query] = dict()
            for i in adv_values[query].keys():
                #Invoke the bots for computing the bids for each advertiser
                adv_bids[query][i] = adv_bots[query][i](i,adv_values[query][i],slot_ctrs[query],history, query, step)
                #If it is the first step or there is at least one advertiser whose bid is different from the bid submitted in the previous step,
                #then we need another iteration, otherwise we can stop
                #print "advertiser: ", i,  " bid: ", str(adv_bids[query][i])
                if step == 0 or adv_bids[query][i] != history[step-1][query]["adv_bids"][i]:
                    done=False
                    
            if done:
                break
        
            #Execute the  FIRST PRICE auction with the bids computed above
            adv_slots, adv_pays = balance(slot_ctrs[query],adv_bids[query], adv_cbudg, adv_sbudg)
            
            #Update budget
            done = True
            for adv in adv_pays:
                #se ogni bidder non ha piu budget mi fermo
                if adv_pays[adv] <  adv_cbudg[adv]:
                    #print adv, " ",  str(adv_pays[adv])
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
            
        print(step, history[step])
        print "\n"

        step += 1
