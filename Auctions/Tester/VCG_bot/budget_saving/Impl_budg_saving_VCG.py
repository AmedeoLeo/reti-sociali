#!/usr/bin/python
output = open("test.txt","w")

def calculate_payment(slot_ctrs, adv_bids, sort_slots,  sort_advs, current):
        sw1=0
        sw2=0
        index = current
        #for current in range(min(len(sort_advs),len(sort_slots))-1):
        while index <min(len(sort_advs),len(sort_slots))-1:
            next_bidder=index +1
            sw1+=adv_bids[sort_advs[next_bidder]] *  slot_ctrs[sort_slots[index]]
            sw2+= adv_bids[sort_advs[next_bidder]] *  slot_ctrs[sort_slots[next_bidder]]
            index+=1
        return sw1-sw2
        
def vcg(slot_ctrs, adv_bids):
    sort_advs=sorted(adv_bids.keys(), key=adv_bids.__getitem__, reverse=True)
    sort_slots=sorted(slot_ctrs.keys(), key=slot_ctrs.__getitem__, reverse=True)
    
    adv_slots = dict()
    adv_pays = dict()
    
    for i in range(min(len(sort_advs),len(sort_slots))):
        adv_slots[sort_advs[i]]=sort_slots[i] #The i-th advertiser takes the i-th slot
        if i == len(sort_advs) - 1: #If it is the last advertiser, the payment is 0
            adv_pays[sort_advs[i]]=0
        else: # Else the payment is the slot of the next advertiser
            #adv_pays[sort_advs[i]]=adv_bids[sort_advs[i+1]]
            #adv_pays[sort_advs[i]]= calculate_payment(sort_slots, sort_advs)
            if i < min(len(sort_advs),len(sort_slots))-1:
                if sort_advs[i] not in  adv_pays:
                    adv_pays[sort_advs[i]]=0
                adv_pays[sort_advs[i]]=calculate_payment(slot_ctrs, adv_bids, sort_slots, sort_advs, i)
                    
    return adv_slots,  adv_pays

def budget_saving_bot(name, adv_value, slot_ctrs, history, query, step):
    #step = len(history)
    print >>output,"\n"
    print >> output,  step
    
    print >> output,  name
    sort_slots=sorted(slot_ctrs.keys(), key=slot_ctrs.__getitem__, reverse=True)
    #If this is the first step there is no history and no best-response is possible
    #We suppose that adevertisers simply bid their value.
    #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
    min_val = adv_value[sort_slots[0]]
    for i in range(len(sort_slots)):
        if min_val > adv_value[sort_slots[i]]:
            min_val = adv_value[sort_slots[i]]
            
    if step == 0:
        return min_val
        #return 0
 
    #Initialization
    #adv_slots=history[step-1][query]["adv_slots"]
    if query not in history[step-1]:
        return
    adv_bids=history[step-1][query]["adv_bids"]
    adv_cbudg=history[step-1][query]["adv_cbudg"]
    
    sort_bids=sorted(adv_bids.values(), reverse=True)
    #sort_slots=sorted(slot_ctrs.keys(), key=slot_ctrs.__getitem__, reverse=True)
    for slot in adv_value:
        print >> output,  "valutazione dello slot ",slot, ": ",  str(adv_value[slot])
    print >> output,"bids precedenti: ",  sort_bids

    payment = min(min_val, sort_bids[len(sort_bids)-1])
    print >> output,"bidder: ", name,  "payment ",  str(payment),  "budget: ",  str(adv_cbudg[name])
    if payment > adv_cbudg[name]:
        return adv_cbudg[name]
    else:
        return payment
   
