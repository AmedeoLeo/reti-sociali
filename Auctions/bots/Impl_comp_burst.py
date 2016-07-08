#!/usr/bin/python

"""Bot which always submits a bid greater than the highest bid seen in previous auc-
tion, even if it is greater than own value"""
def competitor_bursting_bot(name, adv_value, slot_ctrs, history, query, step):
   
   
    #We suppose that adevertisers simply bid 0
    if step == 0:
        return 0
        #return adv_value
   
    epsilon =1
    #Initialization
    adv_bids=history[step-1][query]["adv_bids"]
    adv_cbudg=history[step-1][query]["adv_cbudg"]
    sort_bids=sorted(adv_bids.values(), reverse=True)
    
    #Advs always submit the highest bid augmented by an epsilon value
    payment =sort_bids[0]+epsilon
    if payment > adv_cbudg[name]:
        return adv_cbudg[name]
    else:
        return payment
   
