import json
import datetime
import traceback
import sys
import asyncio

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from pytz import timezone
from datetime import timedelta, datetime

from janaushadi import settings

from order.models import Order
from order.functions import getRetailerById, getComodityById
from order.functions import getCommodityBatch, jsonOfOrderObjectAndOrderItemDetails
from order.functions import sendOrderConfirmationMailToCustomer, get_previous_orders_total_amount
from order.functions import add_order_items_to_order, order_async_functions

from account.models import RetailerShop
from account.functions import get_amount_out_standing

def check_retailer_admin_verified_and_active(retailer_id):
	"""There are some basic conditions you need to met inorder to
		create a order. This function is for checking the integrity of the
		retailer"""
	
	output = {}
	
	try:		
		retailer_obj = getRetailerById(retailer_id)
		if (retailer_obj.is_admin_verified == False) & (retailer_obj.user.is_active == False):
			output['status'] = "failed"
			output['status_error'] = "VERIFICATION_PENDING"
			output['status_text'] = "Verification pending! Please contact "+settings.VIRTUAL_NUMBER+" to verify your account!"
		if retailer_obj.is_admin_verified == False:
			output['status'] = "failed"
			output['status_text'] = "Admin Verification Pending. Please Contact Admin!"
		elif retailer_obj.user.is_active == False:
			output['status'] = "failed"
			output['status_text'] = "Please contact admin on "+settings.VIRTUAL_NUMBER+" to place orders!"
	except ObjectDoesNotExist:
		traceback.print_exc(file=sys.stdout)
		output['status']  = "failed"
		output['status_text'] = "No matching Retailer"
	except Exception as e:
		s = str(e)
		text = s.split(' ',2)[0]
		traceback.print_exc(file=sys.stdout)
		output['status'] = "failed"
		output['status_text'] = text + " doesn't exist, please select correct "+ text +" and try again"
	
	return output

def create_new_order(retailer_obj, created):
    """Creates the new order object."""
    
    grand_total = 0

    new_sales_order = Order.objects.create(
            retailer=retailer_obj, 
            amount=grand_total, 
            pending_amount=grand_total, 
            created=created
    )
    
    year = datetime.today().year
    if datetime.today().month<4:
        year = year-1
    sales_after = "01/" + "04" + "/" + str(year)
    sales_before = str(31)+ "/" + "03" + "/" + str(year+1)
    datetime_start = datetime.strptime(sales_after, "%d/%m/%Y")
    datetime_end = datetime.strptime(sales_before, "%d/%m/%Y") + timedelta(hours=23, minutes=59, seconds=59)
    all_sales_this_day = Order.objects.filter(created__gte=datetime_start, created__lte=datetime_end).all()
    last_company_sale_id = all_sales_this_day[len(all_sales_this_day)-1].id
    
    INVOICE_PREFIX=""
    if settings.INVOICE_PREFIX==None:
        INVOICE_PREFIX=""
	
    new_sales_order.order_no=INVOICE_PREFIX + str(last_company_sale_id+1)
    new_sales_order.save()

    return new_sales_order

def check_batches_quantity(order_items, retailer):
	"""Checks the commodity batches quantity and returns
		the batches that not met the minimum order quantity.
		This also returns batch objects with available quantity is 0.
		This won't let you move forward if the condition not met."""

	under_commodities = {}
	# not_available_commodities = {}
	output = {}
	grand_total = 0

	for item in order_items:
		commodity_obj = getComodityById(int(item['commodityId']))

		for batch in item['batches']:
			commodity_batch_obj = getCommodityBatch(int(batch['id']))
			batch_total_price = batch['qty'] * commodity_batch_obj.price
			grand_total += batch_total_price
			# if batch['qty'] > commodity_batch_obj.available_quantity and batch['qty'] > commodity_obj.available_quantity:
			# 	create_retailer_commodity_req(retailer, commodity_obj)
			# if batch['qty'] > commodity_batch_obj.available_quantity:
			# 	if commodity_obj.commodity.name not in not_available_commodities:
			# 		not_available_commodities[commodity_obj.commodity.name] = [{"batch_id": commodity_batch_obj.id, "current_qty": batch["qty"], "batch_available_quantity": commodity_batch_obj.available_quantity, 'total_quantity': commodity_obj.available_quantity}]
			# 	else:
			# 		not_available_commodities[commodity_obj.commodity.name].append({"batch_id": commodity_batch_obj.id, "current_qty": batch["qty"], "batch_available_quantity": commodity_batch_obj.available_quantity, 'total_quantity': commodity_obj.available_quantity})
			if batch['qty'] < commodity_batch_obj.minimum_order_quantity:
				if commodity_obj.commodity.name not in under_commodities:
					under_commodities[commodity_obj.commodity.name] = [{"batch_id": commodity_batch_obj.id, "minimum_order_qty": commodity_batch_obj.minimum_order_quantity, "current_qty": batch["qty"]}]
				else:
					under_commodities[commodity_obj.commodity.name].append({"batch_id": commodity_batch_obj.id, "minimum_order_qty": commodity_batch_obj.minimum_order_quantity, "current_qty": batch["qty"]})
	
	# if not_available_commodities:
	# 	output['not_available_commodities'] = not_available_commodities
	output["current_order_amount"] = grand_total
	if under_commodities:
		output["under_commodities"] = under_commodities
	return output

def get_order_no(order):
	"""This function will return the invoice no 
		for the order."""

	year = datetime.today().year
	if datetime.today().month < 4:
		year = year-1
	sales_after = "01/"+str('04')+"/"+str(year)
	sales_before = str(31)+"/"+str('03')+"/"+str(year+1)
	datetime_start = datetime.strptime(sales_after, "%d/%m/%Y")
	datetime_end = datetime.strptime(sales_before, "%d/%m/%Y")+timedelta(hours=23,minutes=59,seconds=59)
	allsalesThisFy = Order.objects.filter(created__gte=datetime_start, created__lte=datetime_end).order_by('created').all()
	lastCompanySaleId = allsalesThisFy[len(allsalesThisFy)-1].id
	# print(lastCompanySaleId.id)
	if settings.ORD_Prefix == None:
		settings.ORD_Prefix = ""
	
	return settings.ORD_Prefix + str(lastCompanySaleId+1)

	
@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def confirm_retailer_order(request):
	# data = json.loads(request.data)
	data = request.data
	output = {}
	current_time = timezone('Asia/Kolkata').localize(datetime.now())
	
	try:
		cart_obj = data['cartObj']
		order_items = cart_obj['items']
		retailer_id = data['retailerId']

		try:
			retailer_shop_id = data['retailerShopId']
		except:
			retailer_shop_id = None
			
		is_partial_order_successful = False
		created = timezone('Asia/Kolkata').localize(datetime.now())

		try:
			retailer_shop = RetailerShop.objects.get(id=retailer_shop_id)
		except:
			retailer_shop = None
		
		try:
			send_invoice_to_customer = settings.SEND_INVOICE_TO_CUSTOMER
		except KeyError:
			traceback.print_exc(file=sys.stdout)
			send_invoice_to_customer = True
	except KeyError as e:
		traceback.print_exc(file=sys.stdout)
		s = str(e[0])
		output['status'] = "failed"
		output['status_text'] = "Input fields has one empty field please check and fill it " + s
		return Response(json.dumps(output))
	
	if check_retailer_admin_verified_and_active(retailer_id):
		checked_value = check_retailer_admin_verified_and_active(retailer_id)
		output.update(checked_value)
		return Response(output, status=status.HTTP_400_BAD_REQUEST)
	
	retailer_obj = getRetailerById(retailer_id)

	checked_data = check_batches_quantity(order_items, retailer_obj)

	try:
		if checked_data["under_commodities"]:
			traceback.print_exc(file=sys.stdout)
			output['status'] = 'unknown_error'
			output['status_text'] = 'Internal server error'
			# output['status_msg'] = 'Increase the quantity of the order items and try again'
			output.update(checked_data)
			return Response(output, status=status.HTTP_406_NOT_ACCEPTABLE)
	except KeyError:
		pass

	try:
		#For retailer who needs to pay inorder to complete the order.
		if retailer_obj.is_payment_check_required == True and not retailer_obj.pending_amount_limit:
			output = {}
			current_time = timezone('Asia/Kolkata').localize(datetime.now())

			sgst = 0
			cgst = 0

			order = create_new_order(retailer_obj, current_time)

			items_data, order, grand_total, is_partial_order_successful = add_order_items_to_order(retailer_obj, order, order_items, sgst, cgst)

			if retailer_shop:
				order.address = retailer_shop

			order.amount = grand_total
			order.dispatch_dc = order.retailer.dc
			order.save()

			# if not order.retailer.total_amount_outstanding:
			# 	order.retailer.total_amount_outstanding += grand_total
			# 	order.retailer.save()
			# else:
			# 	order.retailer.total_amount_outstanding = grand_total + 0
			# 	order.retailer.save()

			print("New Grand Total:", order.amount)

			order.order_no = get_order_no(order)
			order.pending_amount = order.amount
			order.save()

			output['newSalesOrder'] = jsonOfOrderObjectAndOrderItemDetails(order)
			output['status'] = "pending_approval"
			output['status_text'] = "Order recorded successfully. Admin will confirm after checking your payment"

			try:
				items_data['ordered_items']
			except KeyError:
				order.status = 'Cancelled'
				order.save()

			try:
				total_other_charges = items_data['total_other_charges']
				total_normal_product_price = items_data['total_normal_product_charges']
			except:
				total_other_charges = 0
				total_normal_product_price = 0

			if is_partial_order_successful:
				output['status'] = "pending_approval_partial_success"
				output['status_text'] = "Order recorded partially. Admin will confirm after checking your payment"
				output['status_msg'] = "There are some items is not in the stock, We will notify you when it arrives"


			asyncio.run(order_async_functions(order, send_invoice_to_customer, total_other_charges, total_normal_product_price, retailer_obj))

			return Response(output, status=status.HTTP_200_OK)
			
		#retailer who have pending amount limit
		elif retailer_obj.is_payment_check_required:
			output = {}
			current_time = timezone('Asia/Kolkata').localize(datetime.now())

			sgst = 0
			cgst = 0

			current_order_amount = checked_data['current_order_amount']
			current_outstanding_amount = get_amount_out_standing(retailer_obj)
			sum_of_order_and_oustanding = current_order_amount + get_previous_orders_total_amount(retailer_obj)

			if sum_of_order_and_oustanding > retailer_obj.pending_amount_limit:
				output["status"] = "order_failed"
				output["status_text"] = f"Your {retailer_obj.pending_amount_limit} credit limit exceeded, please contact admin!"
				output["current_order_amount"] = current_order_amount
				output["pending_amount_limit"] = retailer_obj.pending_amount_limit
				output["current_outstanding_amount"] = current_outstanding_amount
				return Response(output, status=status.HTTP_400_BAD_REQUEST)
			else:
				order = create_new_order(retailer_obj, current_time)

				items_data, order, grand_total, is_partial_order_successful = add_order_items_to_order(retailer_obj, order, order_items, sgst, cgst)
				output.update(items_data)

				if retailer_shop:
					order.address = retailer_shop

				order.amount = grand_total
				order.dispatch_dc = order.retailer.dc
				order.save()

				# if not order.retailer.total_amount_outstanding:
				# 	order.retailer.total_amount_outstanding += grand_total
				# 	order.retailer.save()
				# else:
				# 	order.retailer.total_amount_outstanding = grand_total + 0
				# 	order.retailer.save()

				print("New Grand Total:", order.amount)

				order.order_no = get_order_no(order)
				order.pending_amount = order.amount
				# order.is_admin_verified = True
				order.save()

				output['newSalesOrder'] = jsonOfOrderObjectAndOrderItemDetails(order)
				output['status'] = "pending_approval"
				output['status_text'] = "Order recorded successfully. Admin will confirm after checking your payment"

				try:
					items_data['ordered_items']
				except KeyError:
					order.status = 'Cancelled'
					order.save()

				try:
					total_other_charges = items_data['total_other_charges']
					total_normal_product_price = items_data['total_normal_product_charges']
				except:
					total_other_charges = 0
					total_normal_product_price = 0

				if is_partial_order_successful:
					output['status'] = "pending_approval_partial_success"
					output['status_text'] = "Order recorded partially. Admin will confirm after checking your payment"
					output['status_msg'] = "There are some items is not in the stock, We will notify you when it arrives"

				# out_file, response, is_send = sendOrderConfirmationMailToCustomer(order, send_invoice_to_customer, total_other_charges, total_normal_product_price)
				
				# inv_url = asyncio.run(upload_invoice_to_aws_async(out_file, destination=settings.COMPANY_NAME.replace(" ",""), object_name=(f"{order.id}" + ".pdf")))
				# if inv_url:
				# 	order.inv_url = inv_url
				# 	order.save()
				# 	output["invoice_url"] = inv_url
				# 	send_order_sms(retailer_obj, order, inv_url)

				asyncio.run(order_async_functions(order, send_invoice_to_customer, total_other_charges, total_normal_product_price, retailer_obj))


				return Response(output, status=status.HTTP_200_OK)
		
		#For retailer who verified by the admin who dont have to pay.
		elif retailer_obj.is_payment_check_required == False:
			output = {}
			current_time = timezone('Asia/Kolkata').localize(datetime.now())

			sgst = 0
			cgst = 0

			order = create_new_order(retailer_obj, current_time)

			items_data, order, grand_total,is_partial_order_successful = add_order_items_to_order(retailer_obj, order, order_items, sgst, cgst)
			output.update(items_data)
			print(output)

			if retailer_shop:
				order.address = retailer_shop

			order.amount = grand_total
			order.dispatch_dc = order.retailer.dc
			order.save()

			# if not order.retailer.total_amount_outstanding:
			# 	order.retailer.total_amount_outstanding += grand_total
			# 	order.retailer.save()
			# else:
			# 	order.retailer.total_amount_outstanding = grand_total + 0
			# 	order.retailer.save()


			print("New Grand Total:", order.amount)
			order.order_no = get_order_no(order)
			order.pending_amount = order.amount
			# order.is_admin_verified = True
			order.save()

			output['newSalesOrder'] = jsonOfOrderObjectAndOrderItemDetails(order)
			output['status'] = "pending_approval"
			output['status_text'] = "Order recorded successfully. Admin will verify the order and confirm it"

			try:
				items_data['ordered_items']
			except KeyError:
				order.status = 'Cancelled'
				order.save()

			try:
				total_other_charges = items_data['total_other_charges']
				total_normal_product_price = items_data['total_normal_product_charges']
			except:
				total_other_charges = 0
				total_normal_product_price = 0

			if is_partial_order_successful:
				output['status']="pending_approval_partial_success"
				output['status_text']= "Order placement partially successfull. Please wait for the admin to get verfied"
				output['status_msg'] = "There are some items is not in the stock, We will notify you when it arrives"

			# out_file, response, is_send = sendOrderConfirmationMailToCustomer(order, send_invoice_to_customer, total_other_charges, total_normal_product_price)
			
			# inv_url = asyncio.run(upload_invoice_to_aws_async(out_file, destination=settings.COMPANY_NAME.replace(" ",""), object_name=(f"{order.id}" + ".pdf")))
			# if inv_url:
			# 	order.inv_url = inv_url
			# 	order.save()
			# 	output["invoice_url"] = inv_url
			# 	send_order_sms(retailer_obj, order, inv_url)

			asyncio.run(order_async_functions(order, send_invoice_to_customer, total_other_charges, total_normal_product_price, retailer_obj))

			return Response(output, status=status.HTTP_200_OK)

	except:
		traceback.print_exc(file=sys.stdout)
		output["status"] = 'failed'
		output['status_text'] = "Error occured while adding new Order details please try again"
		return Response(output, status=status.HTTP_400_BAD_REQUEST)
	