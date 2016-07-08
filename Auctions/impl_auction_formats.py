#coding: utf-8
##BALANCED FIRST PRICE##

def balanced_FP(slot_ctrs, adv_bids, adv_cbudgets, adv_sbudgets):
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


##Vickrey–Clarke–Groves##


"""
    This method computes the payments for VCG auction format. Given an adv j and the slot i he won:
        pij = SW (A−j ) − SW (A−i−j)
    where:
        SW(A-i-j) = max social welfare  without j and his slot i
        SW(A-j) = max social welfare without j but with his slot i
"""
def calculate_payment(slot_ctrs, adv_bids, sort_slots,  sort_advs, current):
        sw1=0
        sw2=0
        index = 0
        
        while index <min(len(sort_advs),len(sort_slots))-1:
            if current ==0:
                next=index +1
                sw1+=adv_bids[sort_advs[next]] *  slot_ctrs[sort_slots[index]]
                sw2+=adv_bids[sort_advs[next]] *  slot_ctrs[sort_slots[next]]
                index+=1

            else:
                next=current +1
                if index == current:

                    sw1+=adv_bids[sort_advs[next]] *  slot_ctrs[sort_slots[index]]
                    sw2+= adv_bids[sort_advs[next]] *  slot_ctrs[sort_slots[next]]
                else:

                    sw1+=adv_bids[sort_advs[index]] *  slot_ctrs[sort_slots[index]]
                    sw2+= adv_bids[sort_advs[index]] *  slot_ctrs[sort_slots[index]]
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
        else: # Else the payment is the "damage" done to the next advertiser
            if i < min(len(sort_advs),len(sort_slots))-1:
                if sort_advs[i] not in  adv_pays:
                    adv_pays[sort_advs[i]]=0
                adv_pays[sort_advs[i]]=calculate_payment(slot_ctrs, adv_bids, sort_slots, sort_advs, i)

                    
    return adv_slots,  adv_pays
