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
#We implement a possible bot for an advertiser in a repeated GSP auction
#The bot of an advertiser is a program that, given the history of what occurred in previous auctions, suggest a bid for the next auction.
#Specifically, a bot takes in input
#- the name of the advertiser (it allows to use the same bot for multiple advertisers)
#- the value of the advertiser (it is necessary for evaluating the utility of the advertiser)
#- the clickthrough rates of the slots
#- the history
#We assume the history is represented as an array that contains an entry for each time step,
#i.e. history[i] contains the information about the i-th auction.
#In particular, for each time step we have that 
#- history[i]["adv_bids"] returns the advertisers' bids as a dictionary in which the keys are advertisers' names and values are their bids
#- history[i]["adv_slots"] returns the assignment as a dictionary in which the keys are advertisers' names and values are their assigned slots
#- history[i]["adv_pays"] returns the payments as a dictionary in which the keys are advertisers' names and values are their assigned prices

#The bot that we implement here is a symple best_response bot:
#it completely disregards the history except the last step,
#and suggest the bid that will maximize the advertiser utility
#given that the other advertisers do not change their bids.
def best_response(name, adv_value, slot_ctrs, history, query, step):
    #step = len(history)
    print >>output,"\n"
    print >> output,  step

    print >> output,  name

    #If this is the first step there is no history and no best-response is possible
    #We suppose that adevertisers simply bid their value.
    #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
    if step == 0:
        return 0
    
    #Initialization
    adv_slots=history[step-1][query]["adv_slots"]
    adv_bids=history[step-1][query]["adv_bids"]
    adv_cbudg=history[step-1][query]["adv_cbudg"]
    
    sort_bids=sorted(adv_bids.values(), reverse=True)
    sort_slots=sorted(slot_ctrs.keys(), key=slot_ctrs.__getitem__, reverse=True)
    print >> output,  "valutazioni: ",  adv_value
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
        new_utility = slot_ctrs[sort_slots[i]]*(adv_value-tmp_pay)
        
        if new_utility > utility:
            print >> output,  "vecchia utility ", str(utility),  " nuova utility ",  str(new_utility)
            utility = new_utility
            preferred_slot = i
            payment = tmp_pay
            print >> output, "preferred slot: ", str(i)
            print >> output, "payment ",  str(payment)
    #print name,  " ",  payment, " ", preferred_slot
    #3) Evaluate which bid to choose among the ones that allows the advertiser to being assigned the slot selected at the previous step
    if preferred_slot == -1:
        
        # TIE-BREAKING RULE: I choose the largest bid smaller than my value for which I lose
        return max(adv_value, sort_bids[len(sort_slots)])
    
    if preferred_slot == 0:
       
        # TIE-BREAKING RULE: I choose the bid that is exactly in the middle between my own value and the next bid
        return float(adv_value+payment)/2
 
    #TIE-BREAKING RULE: If I like slot j, I choose the bid b_i for which I am indifferent from taking j at computed price or taking j-1 at price b_i
    return float(adv_value )
    
