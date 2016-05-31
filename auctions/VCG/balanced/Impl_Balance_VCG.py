#!/usr/bin/python

from math import exp 


def calculate_payment(slot_ctrs, adv_bids, sort_slots,  sort_advs, current, query):
        sw1=0
        sw2=0
        index = current
        #for current in range(min(len(sort_advs),len(sort_slots))-1):
        while index <min(len(sort_advs),len(sort_slots))-1:
            next_bidder=index +1
            sw1+=adv_bids[query][sort_advs[next_bidder]] *  slot_ctrs[query][sort_slots[index]]
            sw2+= adv_bids[query][sort_advs[next_bidder]] *  slot_ctrs[query][sort_slots[next_bidder]]
            index+=1
        return sw1-sw2




#Computes the winners when advertisers have a budget.
#It takes in input:
#- the slots' clickthrough rates
#- the advertisers' bids
#- the advertisers' starting budgets
#- the advertisers' current budgets
#- the current query
def balance(slot_ctrs, adv_bids, adv_sbudgets, adv_cbudgets, query):
    query_winners=dict()
    query_pay=dict()
    adv_pays = dict()

    if query not in adv_pays.keys():
       adv_pays[query] = dict()
       
    sorted_slots = sorted(slot_ctrs[query].keys(), key=slot_ctrs[query].__getitem__, reverse=True)
    sorted_revenue = sorted(adv_bids[query].keys(), key=adv_bids[query].__getitem__, reverse=True)
    
    for i in range(min(len(sorted_revenue),len(sorted_slots))):
        if i == len(sorted_revenue) - 1: #If it is the last advertiser, the payment is 0
            adv_pays[query][sorted_revenue[i]]=0
        else:
            if i < min(len(sorted_revenue),len(sorted_slots))-1:
                if sorted_revenue[i] not in  adv_pays:
                    adv_pays[query][sorted_revenue[i]]=0
                adv_pays[query][sorted_revenue[i]]=calculate_payment(slot_ctrs, adv_bids, sorted_slots, sorted_revenue, i, query)
    """
    for query in adv_pays:
        print query
        for adv in adv_pays[query]:
            print adv,  " ",  str(adv_pays[query][adv])
    """
    psi=dict()
    #Only consider advertisers that have a bid for this query
    for advs in adv_bids[query].keys():
        #Only consider advertisers that have enough budget to pay this bid
        
        #We consider only the advertisers that have current budget greater then the amount they should pay 
        #print advs,  " ",  str(adv_cbudgets[advs]),  " ",  str(adv_pays[query][advs])
        if adv_cbudgets[advs] >= adv_pays[query][advs]:
            #The weight assigned to each advertiser is a tradeoff between his bid and the fraction of budget that is still available
            psi[advs] = adv_bids[query][advs]*(1-exp(-adv_cbudgets[advs]/adv_sbudgets[advs]))
            
    #Slots are assigned to advertisers in order of weight (and not simply in order of bid)
    sorted_slot = sorted(slot_ctrs[query].keys(), key=slot_ctrs[query].__getitem__, reverse=True)
    sorted_advs = sorted(psi.keys(), key=psi.__getitem__, reverse = True)
    
    for i in range(min(len(sorted_slot),len(sorted_advs))):
        
        query_winners[sorted_slot[i]] = sorted_advs[i]
        query_pay[sorted_advs[i]] = adv_pays[query][sorted_advs[i]] #Here, use VCG
        print "Il vincitore ", query_winners[sorted_slot[i]], " dello slot ", sorted_slot[i],  " paga "  ,  query_pay[sorted_advs[i]]
        print "-------------------------------------"

    return query_winners, query_pay
    
