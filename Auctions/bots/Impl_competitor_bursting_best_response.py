#!/usr/bin/python

"""Bot which submits the highest possible bid that gives the desired slot"""
def comp_burst_best_response(name, adv_value, slot_ctrs, history, query, step):
  
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
    epsilon = 0.1
    
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
        new_utility = -1
    #2) Evaluate for each slot, which one gives to the advertiser the largest utility
        if sort_slots[i] in adv_value:
        	new_utility = slot_ctrs[sort_slots[i]]*(adv_value[sort_slots[i]]-tmp_pay)
        
        if new_utility > utility:
            utility = new_utility
            preferred_slot = i
        
    #3) Evaluate which bid to choose among the ones that allows the advertiser to being assigned the slot selected at the previous step
    toPay = 0
    if preferred_slot == -1:
        
        # TIE-BREAKING RULE: I bid the maximum value between the last non-winning bid and the average of my values for the slots
        sum1 = 0
        for slot in adv_value:
            sum1 += adv_value[slot]
	if len(adv_value.keys()):
        	toPay = max(sum1/len(adv_value.keys()), sort_bids[len(sort_slots)])
        if toPay < adv_cbudg[name]:
            return toPay
        else:
            return adv_cbudg[name]
    
    if preferred_slot == 0:
       
        # TIE-BREAKING RULE: I bid exactly my value for slot 0
        if adv_value[sort_slots[preferred_slot]] <= adv_cbudg[name]:
            return adv_value[sort_slots[preferred_slot]]
        else:
            return adv_cbudg[name]
 
    #TIE-BREAKING RULE: If I want slot j, I bid the previous bid for slot j-1 decreased by an epsilon value
    toPay = sort_bids[preferred_slot-1]-epsilon
    if toPay <= adv_cbudg[name]:
        return toPay
    else:
        return adv_cbudg[name]
