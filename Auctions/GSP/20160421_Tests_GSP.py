#!/usr/bin/python

from Impl_GSP import gsp

#Slots' clickthrough rates
slot_ctrs=dict()
slot_ctrs["id1"] = 10
slot_ctrs["id2"] = 4

#Advertisers' bids
adv_bids=dict()
adv_bids["x"] = 7
adv_bids["y"] = 6
adv_bids["z"] = 1

adv_slots, adv_pays = gsp(slot_ctrs, adv_bids)

print(adv_slots, adv_pays)
