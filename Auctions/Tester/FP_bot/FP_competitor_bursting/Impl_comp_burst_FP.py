#!/usr/bin/python
output = open("test.txt","w")

def balance(slot_ctrs, adv_bids, adv_cbudgets, adv_sbudgets):
    adv_slots=dict()
    query_pay=dict()
    
    psi=dict()
    
    #Only consider advertisers that have a bid for this query
    for advs in adv_bids.keys():
        #Only consider advertisers that have enough budget to pay this bid
        if adv_cbudgets[advs] >= adv_bids[advs]:
            #The weight assigned to each advertiser is a tradeoff between his bid and the fraction of budget that is still available
            psi[advs] = adv_bids[advs]
            
    #Slots are assigned to advertisers in order of weight (and not simply in order of bid)
    sorted_slot = sorted(slot_ctrs.keys(), key=slot_ctrs.__getitem__, reverse=True)
    sorted_advs = sorted(psi.keys(), key=psi.__getitem__, reverse = True)
    
    for i in range(min(len(sorted_slot),len(sorted_advs))):
        adv_slots[sorted_advs[i]] = sorted_slot[i] #The i-th advertiser takes the i-th slot
        query_pay[sorted_advs[i]] = adv_bids[sorted_advs[i]] #Here, we use first price auction: winner advertisers pay exactly their bid
    
    return adv_slots, query_pay


def competitor_bursting_bot(name, adv_value, slot_ctrs, history, query, step):
    #step = len(history)
    print >>output,"\n"
    print >> output,  step

    print >> output,  name

    #If this is the first step there is no history and no best-response is possible
    #We suppose that adevertisers simply bid their value.
    #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
    if step == 0:
        return 0
        #return adv_value
    epsilon =1
    #Initialization
    #adv_slots=history[step-1][query]["adv_slots"]
    adv_bids=history[step-1][query]["adv_bids"]
    adv_cbudg=history[step-1][query]["adv_cbudg"]
    
    sort_bids=sorted(adv_bids.values(), reverse=True)
    #sort_slots=sorted(slot_ctrs.keys(), key=slot_ctrs.__getitem__, reverse=True)
    for slot in adv_value:
        print >> output,  "valutazione dello slot ",slot, ": ",  str(adv_value[slot])
    print >> output,"bids precedenti: ",  sort_bids

  
    payment =sort_bids[0]+epsilon
    if payment > adv_cbudg[name]:
        #print "------", str(step),  "-------", name, "-----------", str(adv_cbudg[name]), str(payment)
        return adv_cbudg[name]
    else:
        print payment
        return payment
   
