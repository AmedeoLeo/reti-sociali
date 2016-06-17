#!/usr/bin/python

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

                    
    print adv_pays


