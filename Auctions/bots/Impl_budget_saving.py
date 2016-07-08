#!/usr/bin/python

"""Bot which always submits that is the minimum among the last non-winning bid and the
advertiser value for the query"""
def budget_saving_bot(name, adv_value, slot_ctrs, history, query, step):
    
    #If this is the first step we suppose that adevertisers simply bid their minimum value.
    min_val = 1000
    for val in adv_value:
        if min_val > adv_value[val]:
            min_val = adv_value[val]

    if step == 0:
        return min_val
        #return 0
 
    #Initialization
    if query not in history[step-1]:
        return
    adv_bids=history[step-1][query]["adv_bids"]
    adv_cbudg=history[step-1][query]["adv_cbudg"]
    
    sort_bids=sorted(adv_bids.values(), reverse=True)

    payment = min(min_val, sort_bids[len(sort_bids)-1])
    if payment > adv_cbudg[name]:
        return adv_cbudg[name]
    else:
        return payment
   
