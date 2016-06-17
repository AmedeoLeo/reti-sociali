
def gsp(slot_ctrs, adv_bids):
	
	#ordino i bidders in ordine di bid
	sort_advs = sorted(adv_bids.keys(), key = adv_bids.__getitem__, reverse = True)
	sort_slots =  sorted(slot_ctrs.keys(), key = slot_ctrs.__getitem__, reverse = True)
	
	adv_slots = dict()
	adv_pays = dict()
	
	for i in range(min(len(sor_advs),len(sort_slots))):
		adv_slots[sort_advs[i]] = sort_slots[i]
		if i == len(sort_advs) - 1:
			#se è l'ultimo paga 0
			adv_pays[sort_advs[i]] = 0
		else:
			#altrimenti paga la valutazione del succesivo
			adv_pays[sort_advs[i]] = adv_bids[sort_advs[i+1]]
	
	return adv_slots, adv_pays


"""Algoritmo di best response"""
def best_response(name, adv_value, slot_ctrs, history):
	
	step = len(history)
	if step == 0:
		return adv_value
	 
	adv_slots = history[step-1]["adv_slots"]
	adv_bids = history[step-1]["adv_bids"]
	 
	sort_bids = sorted(adv_bids.values(), reverse=True)
	sort_slots =  sorted(slot_ctrs.keys(), key = slot_ctrs.__getitem__, reverse = True)

	#bisogna considerare la bid fatta in precedenza, se l'offerta è più alta di quella 
	#precedente si paga la bid più alta di quella precedente,
	#altrimenti si paga la successiva del corrente
	
	if name not in adv_slots.keys():
		last_slot=-1
	else:
		last_slot = sort_slots.index(adv_slots[name])
	#verifico quale azione mi da utilità più alta
	for i in range(len(sort_slots)):
		#posizione migliore di quella che ho preso prima
		if i < last_slot:
			#paga esattamente quella precedente
			tmp_pay = sort_bids[i]
		elif i < len(sort_bids) - 1:
			#pago la successiva
			tmp_pay = sort_bids[i+1]
		else:
			tmp_pay = 0
			
			
	
		
	return best
