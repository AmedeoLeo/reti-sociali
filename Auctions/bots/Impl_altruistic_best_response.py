#!/usr/bin/python

"""Bot which submits the lowest possible bid that gives the desired slot"""
def altruistic_best_response(name, adv_value, slot_ctrs, history, query, step):
   
    #If this is the first step we suppose that adevertisers simply bid 0.
    if step == 0:
        return 0
    
    #Initialization
    adv_slots=history[step-1][query]["adv_slots"]
    adv_bids=history[step-1][query]["adv_bids"]
    adv_cbudg=history[step-1][query]["adv_cbudg"]
    
    sort_bids=sorted(adv_bids.values(), reverse=True)
    sort_slots=sorted(slot_ctrs.keys(), key=slot_ctrs.__getitem__, reverse=True)

    #Saving the index of slots assigned at the advertiser in the previous auction
    if name not in adv_slots.keys():
        last_slot=-1
    else:
        last_slot=sort_slots.index(adv_slots[name])
        
    utility = -1
    preferred_slot = -1
    payment = 0

    #The best response bot makes the following steps:
    #1) Evaluate for each slot, how much the advertiser would pay if
    #   - he changes his bid so that that slot is assigned to him
    #   - no other advertiser change the bid
    for i in range(len(sort_slots)):
        if i < last_slot: #If I take a slot better than the one previously assigned to me
            tmp_pay = sort_bids[i] #then, I must pay for that slot the bid of the advertiser at which that slot was previously assigned
            
        elif i == len(sort_bids) - 1: #If I take the last slot, I must pay 0
            tmp_pay = 0
            
        else: #If I take the slot as before or a worse one (but not the last)
            tmp_pay = sort_bids[i+1] #then, I must pay for that slot the bid of the next advertiser
        
    #2) Evaluate for each slot, which one gives to the advertiser the largest utility
        new_utility = slot_ctrs[sort_slots[i]]*(adv_value[sort_slots[i]]-tmp_pay)
        
        if new_utility > utility:
            utility = new_utility
            preferred_slot = i
           
    #3) Evaluate which bid to choose among the ones that allows the advertiser to being assigned the slot selected at the previous step
    toPay = 0
    epsilon = 0.1
    if preferred_slot == -1:
        
        # TIE-BREAKING RULE: I bid the minimum between the last previous non-winning bid and the average of my values for the slots
        sum = 0
        for slot in adv_value:
            sum += adv_value[slot]
        return min(sum/len(adv_value), sort_bids[len(sort_slots)])
    
    if preferred_slot == 0:
       
        # TIE-BREAKING RULE: I bid my value for the slot 0
        if payment < adv_value[sort_slots[preferred_slot]]: 
            toPay = payment+epsilon
        else:
           toPay = adv_value[sort_slots[preferred_slot]]
        if toPay > adv_cbudg[name]:
            return adv_cbudg[name]
        else:
            return toPay
 
    #TIE-BREAKING RULE: I bid the minimum value between my value for the slot and the last bid for it (augmented by an epsilon value)
    toPay = min(adv_value[sort_slots[preferred_slot]],  payment+epsilon)
    if toPay > adv_cbudg[name]:
        return adv_cbudg[name]
    else:
        return toPay
    
