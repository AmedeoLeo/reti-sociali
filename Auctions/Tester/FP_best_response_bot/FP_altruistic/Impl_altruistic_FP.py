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

def altruistic_best_response(name, adv_value, slot_ctrs, history, query, step):
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
    
    #Initialization
    adv_slots=history[step-1][query]["adv_slots"]
    adv_bids=history[step-1][query]["adv_bids"]
    adv_cbudg=history[step-1][query]["adv_cbudg"]
    
    sort_bids=sorted(adv_bids.values(), reverse=True)
    sort_slots=sorted(slot_ctrs.keys(), key=slot_ctrs.__getitem__, reverse=True)
    
    for slot in adv_value:
        print >> output,  "valutazione slot ",slot, ": ",   str(adv_value[slot])
    print >> output,"bids precedenti: ",  sort_bids

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
            print >> output,  "vecchia utility ", str(utility),  " nuova utility ",  str(new_utility)
            utility = new_utility
            preferred_slot = i
            payment = tmp_pay
            print >> output, "preferred slot: ", str(i)
            print >> output, "payment ",  str(payment)
   #print name,  " ",  payment, " ", preferred_slot
    #3) Evaluate which bid to choose among the ones that allows the advertiser to being assigned the slot selected at the previous step
    toPay = 0
    epsilon = 0.1
    if preferred_slot == -1:
        
        # TIE-BREAKING RULE: I choose the largest bid smaller than my value for which I lose
        sum = 0
        for slot in adv_value:
            sum += adv_value[slot]
        return min(sum/len(adv_value), sort_bids[len(sort_slots)])
    
    if preferred_slot == 0:
       
        # TIE-BREAKING RULE: I choose the bid that is exactly in the middle between my own value and the next bid
        if payment < adv_value[sort_slots[preferred_slot]]: 
            toPay = payment+epsilon
        else:
           toPay = adv_value[sort_slots[preferred_slot]]
        if toPay > adv_cbudg[name]:
            return adv_cbudg[name]
        else:
            return toPay
 
    #TIE-BREAKING RULE: If I like slot j, I choose the bid b_i for which I am indifferent from taking j at computed price or taking j-1 at price b_i
    toPay = min(adv_value[sort_slots[preferred_slot]],  payment+epsilon)
    if toPay > adv_cbudg[name]:
        return adv_cbudg[name]
    else:
        return toPay
    
