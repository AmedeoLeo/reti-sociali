#!/usr/bin/python

from Impl_VCG import *

#Slots' clickthrough rates
slot_ctrs=dict()
slot_ctrs["id1"] = 10
slot_ctrs["id2"] = 5
slot_ctrs["id3"] = 2

#Advertisers' bids
adv_bids=dict()
adv_bids["x"] = 3
adv_bids["y"] = 2
adv_bids["z"] = 1

#adv_slots, adv_pays = vcg(slot_ctrs, adv_bids)
vcg(slot_ctrs, adv_bids)

#print(adv_slots, adv_pays)
