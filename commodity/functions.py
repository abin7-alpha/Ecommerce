def jsonOfCommodityObject(dc_commodity):
	output={}
	output['id'] = dc_commodity.commodity.id
	output['dc_name'] = dc_commodity.distribution_center.name
	output['dc_id'] = dc_commodity.distribution_center.id
	output['name'] = dc_commodity.commodity.name
	output['measuringUnit'] = dc_commodity.commodity.measuring_unit
	# output['quantityPerCrate'] = commodity.quantityPerCrate
	# output['packing_options'] = commodity.packingByCrateOrBag
	# output['delivery_charge']=commodity.delivery_charge
	#if commodity.additional_quantity!=None:
		#output['additional_quantity']=commodity.additional_quantity
		# output['additional_delivery_charge']=commodity.additional_delivery_charge
	#if commodity.bulk_delivery_charge!=None:
		#output['bulk_delivery_charge']=commodity.bulk_delivery_charge
	output['description'] = dc_commodity.commodity.description
	output['minimum_quantity'] = dc_commodity.minimum_order_quantity
	output['minimumQtyChange'] = dc_commodity.minimum_order_quantity
	output['minimumorderquantity'] = dc_commodity.minimum_order_quantity
	# output['price'] = commodity.todays_price
	# output['offer_price']=commodity.offer_price
	output['priority'] = dc_commodity.commodity.priority
	output['isActive']= dc_commodity.commodity.is_active
	output['available_quantity'] = dc_commodity.available_quantity
	output['min_available_qty'] = dc_commodity.min_available_qty
	output['max_qty_allowed_per_order'] = dc_commodity.max_qty_allowed_per_order
	output['max_available_qty'] = dc_commodity.max_available_qty
	# if commodity.bulk_price!=None:
	# 	output['bulk_price']=commodity.bulk_price
	# if commodity.bulk_qty!=None:
	# 	output['bulk_qty']=commodity.bulk_qty
	if dc_commodity.commodity.image:
		output['image_url'] = dc_commodity.commodity.image.url
		if (dc_commodity.commodity.imageUrl == None):
			dc_commodity.commodity.imageUrl = dc_commodity.commodity.image.url
			dc_commodity.commodity.save()
	if dc_commodity.commodity.imageUrl:
		output['image_url'] = dc_commodity.commodity.imageUrl
	
	return output

def jsonCommodityBatch(batch_obj):
	print(batch_obj)
	output = {}
	output['id'] = batch_obj.id
	output['commodity_name'] = batch_obj.dc_commodity.commodity.name
	output['available_quantity'] = batch_obj.available_quantity
	output['minimum_order_quantity'] = batch_obj.minimum_order_quantity

	return output

def get_moq(available_qty):
	dividents_with_remainder_zero = []

	if available_qty > 100:
		if available_qty % 10 == 0:
			return 10
		elif available_qty % 5 == 0:
			return 5
		elif available_qty % 2 == 0:
			return 2
		return 1
	elif available_qty == 2:
		return 2
	elif available_qty == 3:
		return 3
	elif available_qty == 1:
		return 1
	else:
		for number in range(1, available_qty):
			if available_qty % number == 0:
				dividents_with_remainder_zero.append(number)

		if len(dividents_with_remainder_zero) == 2:
			return dividents_with_remainder_zero[0]
		elif len(dividents_with_remainder_zero) == 3:
			return dividents_with_remainder_zero[1]
		elif len(dividents_with_remainder_zero) == 4:
			return dividents_with_remainder_zero[2]
		elif len(dividents_with_remainder_zero) == 5:
			return dividents_with_remainder_zero[3]
		else:
			return 1
	