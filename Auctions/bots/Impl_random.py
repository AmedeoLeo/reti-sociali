#!/usr/bin/python
from random import randint

"""Bot which always submits a random bid"""
def random_bot(name, adv_value, slot_ctrs, history, query, step):
   
    #We suppose that adevertisers simply bid 0 if it is the first step
    if step == 0:
        return 0
        #return adv_value
 
    #Initialization
    adv_cbudg=history[step-1][query]["adv_cbudg"]

    sum1 = 0
    payment = 0
    
    for slot in adv_value:
        sum1+=adv_value[slot]
        
    #choose a random value between 0 and the average of the values for the slots
    payment = randint(0, int(sum1/len(adv_value.keys())))
        
    if payment > adv_cbudg[name]:
        return adv_cbudg[name]
    else:
        return payment
   
