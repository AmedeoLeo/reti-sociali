#!/usr/bin/python

#Run an experiment in which you look for
#1) an instance (slot_ctrs, adv_values) such that best_response bots never reach an equilibrium
#2) an instance (slot_ctrs, adv_values) such that best_response bots reach different equilibria when initial bidding are different

#Try different tie-breaking rules in the best_response bot and run the same experiments as above for these modified bots

#BONUS: Suppose that the *final utility* of advertisers is defined as
#       0 if an equilibrium has not been reached,
#       otherwise it is the the utility received in the last step.
#       Fix an advertiser and suppose that the other advertisers use the best_response bot.
#       Develop a bot for the fixed advertiser that returns a final utility
#       better than the one achieved by using the best_response bot

