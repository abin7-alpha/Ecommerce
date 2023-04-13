import traceback
import sys
import pytz
import math
import pdfkit
import boto3
import logging
import os
import asyncio

from janaushadi import settings

from pyshorteners import Shortener

from datetime import datetime
from pytz import timezone

from django.db.models import Sum, Q
from django.http import HttpResponse

from account.models import Retailer, RetailerDevice, RetailerCommodityRequests, Staff, RetailerNotification, NotificationType
from account.functions import send_mails, send_sms, send_notification
from account.api.serializers.retailer_shop import RetailerShopSerializer

from commodity.models import DcCommodity, DcCommodityBatch
from commodity.functions import jsonOfCommodityObject, jsonCommodityBatch

from order.models import OrderItem, Order, RetailerPayment
from order.api.serializers.order_item import OrderItemSerializer
from order.html_snippets import confirm_order_template, order_msg_template, updated_order_msg_template, order_msg_verfied_template, stock_availability_staff_notify_email
from order.html_snippets import order_shipped_email_template, order_shipped_sms_template, order_delivered_email_template, order_delivered_sms_template
from order.html_snippets import order_canceled_email_template, order_canceled_sms_template

from boto.s3.connection import S3Connection
from botocore.exceptions import ClientError

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from commodity.models import DcCommodity, DcCommodityBatch, DistributionStoreIndent
from commodity.api.serializers.dc_commodity import DcCommoditySerializer

from office.models import DistributionCenter

def create_notification(retailer, message_desc, title, not_type):
	notification_type = NotificationType.objects.get(name=not_type)

	notification = RetailerNotification.objects.create(
		retailer=retailer,
		title=title,
		content=message_desc,
		notification_type=notification_type,
		app_name='Retailer_Web'
	)

	return notification

def getRetailerById(retailerId):	
	retailerObj=None
	retailerObj=Retailer.objects.get(id=retailerId)
	return retailerObj

def getComodityById(commodityId):
	commodityObj=None
	commodityObj = DcCommodity.objects.get(id=commodityId)
	return commodityObj

def getCommodityBatch(commodity_batch_id):
	try:
		commodity_batch = DcCommodityBatch.objects.get(id=commodity_batch_id)
	except:
		commodity_batch = None
	return commodity_batch

def checkifAllOrderItemsInStock(orderItems):
	result={}
	for orderItem in orderItems:
		commodityId=orderItem['id']
		commodityObj=getComodityById(commodityId)
		commodityOrderQuantity=orderItem['orderQty']
		if commodityOrderQuantity>commodityObj.available_quantity:
			result['isAllItemsInStock']=False
			result['outOfStockItem']=commodityObj
			return result
	result['isAllItemsInStock']=True
	return result

bitly_access_token="b664085823d098b512126528f27f53cd39b562de"

def jsonOfOrderObjectAndOrderItemDetails(order):
	orderJson={}
	orderJson['id']=order.id
	orderJson['retailer_name']=order.retailer.user.name
	orderJson['retailer_phone']=order.retailer.user.phone
	orderJson['isStaffFeedBackProvided']=order.is_staff_feed_back_provided
	try:
		orderJson['address'] = RetailerShopSerializer(order.address).data
	except:
		orderJson['address'] = None
	# orderJson['noCratesDelivered']=order.noCratesDelivered
	# orderJson['noCratesCollected']=order.noCratesCollected
	# orderJson['retailer_shop_name']=order.retailer.shop_name
	orderJson['isPostConfirmationRequired']=order.is_post_confirmation_required
	orderJson['retailer_position']={}
	if order.retailer.position!=None:
		print(order.retailer.position.latitude);
		orderJson['retailer_position']['latitude']=float(order.retailer.position.latitude)
		orderJson['retailer_position']['longitude']=float(order.retailer.position.longitude)
	orderJson['retailer_id']=order.retailer.id
	orderJson['amount']=order.amount
	# orderJson['delivery_charges']=order.delivery_charges
	orderJson['pendingAmount']=order.pending_amount
	orderJson['created']=order.created.astimezone(pytz.timezone('Asia/Kolkata')).strftime("%b %d %Y %H:%M:%S")
	if order.delivery_time!=None:
		orderJson['deliveryTime']=order.delivery_time.astimezone(pytz.timezone('Asia/Kolkata')).strftime("%b %d %Y %H:%M:%S")
	orderJson['status']=order.status
	orderJson['orderNo']=order.order_no
	if order.inv_url:
		orderJson['invURL']=order.inv_url
		if order.inv_url.endswith('.pdf')==False:
			try:
				shortener = Shortener('Bitly', bitly_token=bitly_access_token,timeout=9000)
				# print("My long url is {}".format(shortener.expand(order.invURL)))
				orderJson['invURL']=format(shortener.expand(order.inv_url))
			except:
				print("Error expanding url")

	else:
		orderJson['invURL']=""

	orderJson['numberOfItems']=len(order.order_items.filter(~Q(status='Out_Of_Stock')).all())
	return orderJson

def getOrderItemsTable(saleOrder, total_cost):
	# <tr style="background-color:lightgray;"><th colspan="10"><h3 align="center" > Order Summary</h3></th></tr>
	table="""<table cellspacing="10" style="width: 100%;font-weight: 200">
				

		<thead>
			<tr>			
				<th>Sr.</th>
				<th>Product Name</th>
				<th>Unit</th>
				<th>HSN</th>
				<th>Batch</th>
				<th>Qty</th>
				<th>Exp Date</th>
				<th>MRP</th>
				<th>Rate</th>
				<th>CGST</th>
				<th>SGST</th>
				<th>IGST</th>
				<th>Amount</th>
			</tr>		
		</thead>""" 
	count = 1
	sgst = 0
	cgst = 0
	for orderitem in saleOrder.order_items.filter(~Q(status='Out_Of_Stock')).all():
		print("Item price: ",str(orderitem.price))
		if settings.IS_GST_APPLICABLE:
			totalProductPrice = round(orderitem.price+(orderitem.price*(orderitem.commodity.commodity.gst/100)),2)
			print("Gross Product price: ",str(totalProductPrice))
		else:
			totalProductPrice = orderitem.price
			print("Gross Product price: ",str(totalProductPrice))

		# below code not needed as the price attached to item is after discount

		try:
			mrp = orderitem.commodity_batch.mrp
		except:
			mrp = 0

		exp_date = datetime.strftime(orderitem.commodity_batch.expiry_date, "%d/%m/%Y")

		grossItemCost=round(orderitem.quantity*orderitem.price,2)
		sgst = round((float(orderitem.price * orderitem.quantity) * orderitem.commodity.commodity.gst/ 200), 2)
		cgst = round((float(orderitem.price * orderitem.quantity) * orderitem.commodity.commodity.gst/ 200), 2)
		# No Deliver Charge At Individual Level
		# <th align="left">"""+str(orderitem.quantity*orderitem.delivery_charge)+"""</th>
		table+="""
				<tr style="border-bottom:1px solid black">
					<th class="line" align="left">"""+ str(count) +"""</th>
					<th class="line" align="left">"""+orderitem.commodity.commodity.name +"""</th>
					<th class="line" align="left">"""+ orderitem.commodity.commodity.measuring_unit.name +"""</th>
					<th class="line" align="left">"""+ orderitem.commodity.commodity.hsncode +"""</th>
					<th class="line" align="left">""" + str(orderitem.commodity_batch.batch_id) + """</th>
					<th class="line" align="left">"""+str(int(orderitem.quantity))+"""</th>
					<th class="line" align="left">""" + str(exp_date) + """</th>
					<th class="line" align="left">"""+str(mrp)+"""</th>
					<th class="line" align="left">"""+str(orderitem.price)+"""</th>
					<th class="line" align="left">"""+ str(sgst) + str(f"({str(round(orderitem.commodity.commodity.gst/2, 2))})") +"""</th> 
					<th class="line" align="left">"""+ str(cgst) + str(f"({str(round(orderitem.commodity.commodity.gst/2, 2))})") +"""</th> 
					<th class="line" align="left">"""+ str("0.00(0.00)") +"""</th> 
					<th class="line" align="left">"""+str(grossItemCost)+"""</th> 
				</tr>"""
		count += 1
	table+="</table>"	
	return table

def getFinalTaxContent(saleOrder):
	sgst=0
	cgst=0
	igst=0
	total_cost=0
	if settings.IS_GST_APPLICABLE:
		for orderitem in saleOrder.order_items.filter(~Q(status='Out_Of_Stock')).all():
			sgst += round((float(orderitem.price * orderitem.quantity) * orderitem.commodity.commodity.gst/ 200), 2)
			cgst += round((float(orderitem.price * orderitem.quantity) * orderitem.commodity.commodity.gst/ 200), 2)
			totalProductPrice=round(orderitem.price+(orderitem.price*(orderitem.commodity.commodity.gst/100)),2)
			total_cost+=(totalProductPrice * orderitem.quantity)
			print("total_cost", total_cost, " sgst", sgst, " cgst", cgst)
		taxContent="""<div class="line" style="width:100%;margin-right:50px;text-align:right;font-weight:400">
											<h5>TOTAL SGST : Rs.""" + str(round(sgst, 2)) + """</h5>
											<h5>TOTAL CGST : Rs.""" + str(round(cgst, 2)) + """</h5>
											<h5>TOTAL COST : Rs.""" + str(round(total_cost, 2)) + """</h5>
										</div>"""
	else:
		for orderitem in saleOrder.order_items.all():
			totalProductPrice=round(orderitem.price,2)
			total_cost+=round((totalProductPrice * orderitem.quantity),2)
		taxContent="""<div style="width:100%;margin-right:50px;text-align:right">
										</div>"""
	return taxContent

def send_updated_order_sms(retailer, order, invoice):
	output = {}
	app_name = settings.APP_NAME
	user_name = retailer.user.name
	order_id = str(order.order_no)
	total_order_items = order.get_total_products
	total_amount = order.amount
	phone_number = f'91{retailer.user.phone}'

	msg = updated_order_msg_template.substitute(
		user_name=user_name, 
		app_name=app_name, 
		order_id=order_id,
		total_order_items=total_order_items,
		total_amount=total_amount,
		invoice=str(invoice)
	)

	print('message:', msg, 'phone_number', phone_number)

	send_sms(msg, phone_number)

	output["isSent"] = True
	return output


async def send_browser_alert(retailer, message_desc, message_title):
	print("sending browser alert")
	retailer_devices = RetailerDevice.objects.filter(retailer=retailer)
	to_lang = retailer.prefered_lang_code
	for device in retailer_devices:
		fcm_token = device.fcm_token
		send_notification(fcm_token, message_desc, message_title, to_lang)

async def send_order_sms(retailer, order, invoice):
	output = {}
	app_name = settings.APP_NAME
	user_name = retailer.user.name
	order_id = str(order.order_no)
	total_order_items = order.get_total_products
	total_amount = order.amount
	phone_number = f'91{retailer.user.phone}'

	msg = order_msg_template.substitute(
		user_name=user_name, 
		app_name=app_name, 
		order_id=order_id,
		total_order_items=total_order_items,
		total_amount=total_amount,
		invoice=str(invoice)
	)

	print('message:', msg, 'phone_number', phone_number)

	send_sms(msg, phone_number)

	output["isSent"] = True
	return output

async def send_shipped_email(retailer, order, notes):
	note = ""
	if notes:
		note = notes
	recipient = retailer.user.email
	user_name = retailer.user.name

	body_html = order_shipped_email_template.substitute(
			user_name=user_name, 
			order_no=str(order.order_no), 
			note=note
	)
	
	subject = "Mahaveer Drug House : Order Shipped"
    # The email body for recipients with non-HTML email clients.

	body_text = (
		"Hai! This is Mahaveer Drug House\r\n"
	)

	value = send_mails(recipient, body_html, body_text, subject)

	return value

async def send_canceled_email(retailer, order, notes):
	note = ""
	if notes:
		note = notes
	recipient = retailer.user.email
	user_name = retailer.user.name

	body_html = order_canceled_email_template.substitute(
			user_name=user_name, 
			order_no=str(order.order_no), 
			note=note
	)
	
	subject = "Mahaveer Drug House : Order Canceled"
    # The email body for recipients with non-HTML email clients.

	body_text = (
		"Hai! This is Mahaveer Drug House\r\n"
	)

	value = send_mails(recipient, body_html, body_text, subject)

	return value

async def send_delivered_email(retailer, order):
	recipient = retailer.user.email
	user_name = retailer.user.name

	body_html = order_delivered_email_template.substitute(
			user_name=user_name, 
			order_no=str(order.order_no), 
	)
	
	subject = "Mahaveer Drug House : Order Delivered"
    # The email body for recipients with non-HTML email clients.

	body_text = (
		"Hai! This is Mahaveer Drug House\r\n"
	)

	value = send_mails(recipient, body_html, body_text, subject)

	return value

async def send_shipped_sms(retailer, order, notes):
	note = ""
	if notes:
		note = notes
	output = {}
	user_name = retailer.user.name
	phone_number = f'91{retailer.user.phone}'

	msg = order_shipped_sms_template.substitute(
		user_name=user_name, 
		order_no=str(order.order_no),
		note = note
	)

	print('message:', msg, 'phone_number', phone_number)

	send_sms(msg, phone_number)

	output["isSent"] = True
	return output

async def send_canceled_sms(retailer, order, notes):
	note = ""
	if notes:
		note = notes
	output = {}
	user_name = retailer.user.name
	phone_number = f'91{retailer.user.phone}'

	msg = order_canceled_sms_template.substitute(
		user_name=user_name, 
		order_no=str(order.order_no),
		note = note
	)

	print('message:', msg, 'phone_number', phone_number)

	send_sms(msg, phone_number)

	output["isSent"] = True
	return output

async def send_delivered_sms(retailer, order):
	output = {}
	user_name = retailer.user.name
	phone_number = f'91{retailer.user.phone}'

	msg = order_delivered_sms_template.substitute(
		user_name=user_name, 
		order_no=str(order.order_no),
	)

	print('message:', msg, 'phone_number', phone_number)

	send_sms(msg, phone_number)

	output["isSent"] = True
	return output

async def send_order_verfied_sms(retailer, order, invoice):
	output = {}
	app_name = settings.APP_NAME
	user_name = retailer.user.name
	order_id = str(order.order_no)
	total_order_items = order.get_total_products
	total_amount = order.amount
	phone_number = f'91{retailer.user.phone}'

	msg = order_msg_verfied_template.substitute(
		user_name=user_name, 
		app_name=app_name, 
		order_id=order_id,
		total_order_items=total_order_items,
		total_amount=total_amount,
		invoice=str(invoice)
	)

	print('message:', msg, 'phone_number', phone_number)

	send_sms(msg, phone_number)

	output["isSent"] = True
	return output

def send_mail_with_attachment(recipient, body_html, body_text, subject, file_obj_path):
	"""The function will send the email with attachement.
		You can get the file_obj_path using 		
		path = os.getcwd()
		file_obj_path = os.path.join(path, file_name)
	"""
	
	output = {}

	client = boto3.client(
        'ses',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.SNS_REGION
    )

	SENDER = settings.SENDER_EMAIL
	RECIPIENT = recipient
	ATTACHMENT = file_obj_path
	SUBJECT = subject
	BODY_TEXT = body_text
	BODY_HTML = body_html
	CHARSET = "utf-8"

	# Create a multipart/mixed parent container.
	msg = MIMEMultipart('mixed')
	# Add subject, from and to lines.
	msg['Subject'] = SUBJECT 
	msg['From'] = SENDER 
	msg['To'] = RECIPIENT

	# Create a multipart/alternative child container.
	msg_body = MIMEMultipart('alternative')

	# Encode the text and HTML content and set the character encoding. This step is
	# necessary if you're sending a message with characters outside the ASCII range.
	textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
	htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)

	# Add the text and HTML parts to the child container.
	msg_body.attach(textpart)
	msg_body.attach(htmlpart)

	# Define the attachment part and encode it using MIMEApplication.
	att = MIMEApplication(open(ATTACHMENT, 'rb').read())

	# Add a header to tell the email client to treat this part as an attachment,
	# and to give the attachment a name.
	att.add_header('Content-Disposition','attachment',filename=f'invoice_{os.path.basename(ATTACHMENT)}')

	# Attach the multipart/alternative child container to the multipart/mixed
	# parent container.
	msg.attach(msg_body)

	# Add the attachment to the parent container.
	msg.attach(att)
	try:
		#Provide the contents of the email.
		response = client.send_raw_email(
			Source=SENDER,
			Destinations=[
				RECIPIENT
			],
			RawMessage={
				'Data':msg.as_string(),
			}
		)
	except ClientError as e:
		print(e.response['Error']['Message'])
	else:
		print("Email sent! Message ID:"),
		output['message_id'] = response['MessageId']
		return output
	
def sendUpdatedOrderConfirmationMailToCustomer(saleOrder, sendInvoiceToCustomer):
	retailer = saleOrder.retailer
	retailer_user_name = retailer.user.name
	
	try:
		retailer_shop_name = saleOrder.address.shop_name
	except:
		retailer_shop_name = " "

	total_cost = str(saleOrder.amount)
	total_delivery_cost = str(0)
	order_items_table = getOrderItemsTable(saleOrder, total_cost)
	final_tax_content = getFinalTaxContent(saleOrder)
	final_cost = str(math.ceil(saleOrder.amount) + 0)
	order_time = saleOrder.created.astimezone(pytz.timezone('Asia/Kolkata')).strftime("%b %d %Y %H:%M:%S")
	
	try:
		primary_color = settings.PRIMARY_COLOR
	except:
		primary_color = 'blue'

	try:
		logo_url = settings.COMPANY_LOGO
	except:
		logo_url = ''

	company_name = settings.COMPANY_NAME
	company_url = settings.COMPANY_URL
	company_address = settings.COMPANY_ADDRESS
	company_billing_name = settings.COMPANY_BILLING_NAME

	customer_add_on_details = ""
	if(saleOrder.retailer.user.phone != None):
		customer_add_on_details = customer_add_on_details + saleOrder.retailer.user.phone
	elif(saleOrder.retailer.user.email != None):
		customer_add_on_details = customer_add_on_details + saleOrder.retailer.user.email

	invoice_number = str(saleOrder.id)
	if saleOrder.order_no != None:
		invoice_number = saleOrder.order_no

	body_html = confirm_order_template.substitute(
			primary_color=primary_color, 
			logo_url=logo_url, 
			company_billing_name=company_billing_name, 
			order_time=str(order_time),
			invoice_number=str(invoice_number),
			retailer_user_name=retailer_user_name,
			retailer_shop_name=retailer_shop_name,
			customer_add_on_details=customer_add_on_details,
			total_cost=total_cost,
			order_items_table=order_items_table,
			final_tax_content=final_tax_content,
			total_delivery_cost=total_delivery_cost,
			final_cost=final_cost,
			company_name=company_name,
			company_address=company_address,
			company_url=company_url
	)
	
	subject = "Mahaveer Drug House : Admin Edited Order Confirmation"
    # The email body for recipients with non-HTML email clients.

	body_text = (
		"Hai! This is Mahaveer Drug House\r\n"
	)
	
	recipient = retailer.user.email

	try:
		out_file, file_name = convert_html_to_pdf(invoice_number, body_html)
		path = os.getcwd()
		file_obj_path = os.path.join(path, file_name)
		value = send_mail_with_attachment(recipient, body_html, body_text, subject, file_obj_path)
		is_send = True
		return out_file, value, is_send

	except:
		traceback.print_exc(file=sys.stdout)
		out_file = None
		value = None
		is_send = False
		return out_file, value, is_send

def get_order_data(order):
	grand_total = 0
	total_other_charges = 0
	total_normal_product_price = 0

	for order_item in order.order_items:
		total_quantity_batch_price = order_item.quantity * order_item.commodity_batch.price
		# commodity_order_quantity = order_item.quantity
		price = order_item.commodity_batch.price

		order_item['orderItemTotal'] = total_quantity_batch_price
		
		order.delivery_charge = 0
		total_other_charges += order_item.sgst + order_item.cgst
		total_normal_product_price += price * order.quantity
		total_product_price = round(order_item.price+(order_item.price * (order_item.commodity.commodity.gst / 100)), 2)
		order_item['orderItemTotal'] = (total_product_price * order_item.quantity)
		grand_total += order_item['orderItemTotal']
	
	return total_other_charges, grand_total, total_normal_product_price

def get_stock_low_commodities_html(commodities):
	print("stock email sended -----")
	table="""<table cellspacing="10" style="width: 100%;font-weight: 200">
		<thead>
			<tr>			
				<th>Sr.</th>
				<th>Product Name</th>
				<th>Unit</th>
				<th>HSN</th>
			</tr>		
		</thead>""" 
	count = 1
	for commodity in commodities:
		table+="""
				<tr style="border-bottom:1px solid black">
					<th class="line" align="left">"""+ str(count) +"""</th>
					<th class="line" align="left">"""+commodity.commodity.name +"""</th>
					<th class="line" align="left">"""+ commodity.commodity.measuring_unit.name +"""</th>
					<th class="line" align="left">"""+ commodity.commodity.hsncode +"""</th>
				</tr>"""
		count += 1
	table+="</table>"	
	return table

def send_mail_needed_commodities_list(commodity):
	print("sending refill commodity......")
	try:
		primary_color = settings.PRIMARY_COLOR
	except:
		primary_color = 'blue'

	try:
		logo_url = settings.COMPANY_LOGO
	except:
		logo_url = ''
	
	company_name = settings.COMPANY_NAME
	company_url = settings.COMPANY_URL
	company_address = settings.COMPANY_ADDRESS
	company_billing_name = settings.COMPANY_BILLING_NAME

	body_html = stock_availability_staff_notify_email.substitute(
			primary_color=primary_color, 
			logo_url=logo_url, 
			company_billing_name=company_billing_name, 
			company_name=company_name,
			company_address=company_address,
			company_url=company_url,
			commodity_name=commodity.commodity.name,
			minimum_available_quantity=str(commodity.min_available_qty ),
			available_quantity=str(commodity.available_quantity)
	)
	
	subject = "Mahaveer Drug House : Stock Low Commodity"
    # The email body for recipients with non-HTML email clients.

	body_text = (
		"Hai! This is Mahaveer Drug House\r\n"
	)
	
	recipient = "abinpaul00007@gmail.com"

	send_mails(recipient, body_html, body_text, subject)
	

async def quantity_needed_commodities_sent_email(order):
	order_tems = order.order_items.all()
	print("stock email sending -----")
	current_date_time = timezone('Asia/Kolkata').localize(datetime.now())
	inventory_staff = Staff.objects.get(is_logistics_manager=True)
	for instance in order_tems:
		print(instance.commodity.commodity.name)
		print(instance.commodity.available_quantity, "available quantity")
		print(instance.commodity.min_available_qty, "min available quantity")
		if instance.commodity.available_quantity <= instance.commodity.min_available_qty:
			instance.commodity.last_availability_notified = current_date_time
			instance.commodity.save()
			send_mail_needed_commodities_list(instance.commodity)

async def sendOrderConfirmationMailToCustomer(saleOrder, total_other_charges, total_normal_product_price):
	retailer = saleOrder.retailer
	retailer_user_name = retailer.user.name
	
	try:
		retailer_shop_name = saleOrder.address.shop_name
	except:
		retailer_shop_name = " "

	total_cost = str(round(total_normal_product_price, 2))
	total_delivery_cost = str(0)
	order_items_table = getOrderItemsTable(saleOrder, total_cost)
	final_tax_content = getFinalTaxContent(saleOrder)
	final_cost = str(round(saleOrder.amount, 2))
	order_time = saleOrder.created.astimezone(pytz.timezone('Asia/Kolkata')).strftime("%b %d %Y %H:%M:%S")
	
	try:
		primary_color = settings.PRIMARY_COLOR
	except:
		primary_color = 'blue'

	try:
		logo_url = settings.COMPANY_LOGO
	except:
		logo_url = ''

	company_name = settings.COMPANY_NAME
	company_url = settings.COMPANY_URL
	company_address = settings.COMPANY_ADDRESS
	company_billing_name = settings.COMPANY_BILLING_NAME

	customer_add_on_details = ""
	if(saleOrder.retailer.user.phone != None):
		customer_add_on_details = customer_add_on_details + saleOrder.retailer.user.phone
	elif(saleOrder.retailer.user.email != None):
		customer_add_on_details = customer_add_on_details + saleOrder.retailer.user.email

	invoice_number = str(saleOrder.id)
	if saleOrder.order_no != None:
		invoice_number = saleOrder.order_no

	body_html = confirm_order_template.substitute(
			primary_color=primary_color, 
			logo_url=logo_url, 
			company_billing_name=company_billing_name, 
			order_time=str(order_time),
			invoice_number=str(invoice_number),
			retailer_user_name=retailer_user_name,
			retailer_shop_name=retailer_shop_name,
			customer_add_on_details=customer_add_on_details,
			total_cost=total_cost,
			order_items_table=order_items_table,
			final_tax_content=final_tax_content,
			total_delivery_cost=total_delivery_cost,
			final_cost=final_cost,
			company_name=company_name,
			company_address=company_address,
			company_url=company_url,
			other_charges=str(total_other_charges)
	)
	
	subject = "Mahaveer Drug House : Order Verfied"
    # The email body for recipients with non-HTML email clients.

	body_text = (
		"Hai! This is Mahaveer Drug House\r\n"
	)
	
	recipient = retailer.user.email

	file_name = str(invoice_number) + '.pdf'
	path = os.getcwd()
	file_obj_path = os.path.join(path, file_name)
	print("file object path:", file_obj_path)

	message_desc = "Your order has been approved by the admin"
	message_title = "MAHAVEER DRUG HOUSE: Order Approved"
	title = "Order Approved"
	notification_type = 'myorders'

	create_notification(retailer, message_desc, title, notification_type)

	value = send_mail_with_attachment(recipient, body_html, body_text, subject, file_obj_path)
	asyncio.create_task(send_order_sms(retailer, saleOrder, saleOrder.inv_url))
	asyncio.create_task(send_browser_alert(retailer, message_desc, message_title))
	asyncio.create_task(quantity_needed_commodities_sent_email(saleOrder))

async def create_pdf(saleOrder, sendInvoiceToCustomer, total_other_charges, total_normal_product_price):
	# print(total_normal_product_price, total_other_charges, ".......................")
	retailer = saleOrder.retailer
	retailer_user_name = retailer.user.name
	
	try:
		retailer_shop_name = saleOrder.address.shop_name
	except:
		retailer_shop_name = " "

	total_cost = str(round(total_normal_product_price, 2))
	total_delivery_cost = str(0)
	order_items_table = getOrderItemsTable(saleOrder, total_cost)
	final_tax_content = getFinalTaxContent(saleOrder)
	final_cost = str(round(saleOrder.amount, 2))
	order_time = saleOrder.created.astimezone(pytz.timezone('Asia/Kolkata')).strftime("%b %d %Y %H:%M:%S")
	
	try:
		primary_color = settings.PRIMARY_COLOR
	except:
		primary_color = 'blue'

	try:
		logo_url = settings.COMPANY_LOGO
	except:
		logo_url = ''

	company_name = settings.COMPANY_NAME
	company_url = settings.COMPANY_URL
	company_address = settings.COMPANY_ADDRESS
	company_billing_name = settings.COMPANY_BILLING_NAME

	customer_add_on_details = ""
	if(saleOrder.retailer.user.phone != None):
		customer_add_on_details = customer_add_on_details + saleOrder.retailer.user.phone
	elif(saleOrder.retailer.user.email != None):
		customer_add_on_details = customer_add_on_details + saleOrder.retailer.user.email

	invoice_number = str(saleOrder.id)
	if saleOrder.order_no != None:
		invoice_number = saleOrder.order_no

	body_html = confirm_order_template.substitute(
			primary_color=primary_color, 
			logo_url=logo_url, 
			company_billing_name=company_billing_name, 
			order_time=str(order_time),
			invoice_number=str(invoice_number),
			retailer_user_name=retailer_user_name,
			retailer_shop_name=retailer_shop_name,
			customer_add_on_details=customer_add_on_details,
			total_cost=total_cost,
			order_items_table=order_items_table,
			final_tax_content=final_tax_content,
			total_delivery_cost=total_delivery_cost,
			final_cost=final_cost,
			company_name=company_name,
			company_address=company_address,
			company_url=company_url,
			other_charges=str(total_other_charges)
	)
	
	subject = "Mahaveer Drug House : Order Confirmation"
    # The email body for recipients with non-HTML email clients.

	body_text = (
		"Hai! This is Mahaveer Drug House\r\n"
	)
	
	recipient = retailer.user.email

	try:
		out_file, file_name = convert_html_to_pdf(invoice_number, body_html)
		path = os.getcwd()
		file_obj_path = os.path.join(path, file_name)
		print("file object path:", file_obj_path)
		value = send_mail_with_attachment(recipient, body_html, body_text, subject, file_obj_path)
		is_send = True
		return out_file, file_obj_path

	except:
		traceback.print_exc(file=sys.stdout)
		out_file = None
		value = None
		is_send = False
		file_obj_path = False
		return out_file, file_obj_path
		
def convert_html_to_pdf(invoice_number, message):
	# file_save_path = '/home/abin/Documents/Tudo/janaushadi/kendra/MDHBackendRepo/media/invoices'
	filename = str(invoice_number) + '.pdf'
	# complete_filename = os.path.join(file_save_path, filename)
	config = pdfkit.configuration(wkhtmltopdf=settings.HTML2PDF_PATH)
	options = {'encoding': "UTF-8", 'no-outline': None, "enable-local-file-access": None}
	pdf = pdfkit.from_string(message, filename, configuration=config, options=options)

	outfile = open(filename, "ab+")

	return outfile, filename

async def order_async_functions(order, send_invoice_to_customer, total_other_charges, total_normal_product_price, retailer_obj):
	mail_task = asyncio.create_task(create_pdf(order, send_invoice_to_customer, total_other_charges, total_normal_product_price))

	out_file, file_obj_path = await mail_task
	print(out_file, "outfile")
			
	inv_url = asyncio.create_task(upload_invoice_to_aws(out_file, destination=settings.COMPANY_NAME.replace(" ",""), object_name=(f"{order.id}" + ".pdf")))
	if await inv_url:
		if os.path.isfile(file_obj_path):
			os.remove(file_obj_path)
		order.inv_url = await inv_url
		order.save()
		asyncio.create_task(send_order_sms(retailer_obj, order, order.inv_url))

	print("async func finished....")
	# task = asyncio.create_task(upload_invoice_to_aws(file_obj, destination, object_name))
	# value = task.result()
	# return value

async def upload_invoice_to_aws(file_obj, destination, object_name):
	bucket = settings.AWS_STORAGE_BUCKET_NAME
	folder_name = destination
	name_prefix = str((datetime.now() - datetime(1970,1,1)).total_seconds()).split(".")[0]
	print(name_prefix)
	object_name = name_prefix + "-" + object_name
	# full_file_name = os.path.join(
	#     folder_name,
	#     object_name
	# )
	print(object_name)
	# Upload the file

	s3_client = boto3.client(
		's3',
		aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
		aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY
	)

	try:
		url = ""
		pathName = folder_name + "/" + object_name
		fileContent=file_obj.read()
		file_obj.seek(0)
		print("seeked", file_obj)
		s3_client.upload_fileobj(file_obj, bucket, pathName)
		url = settings.BASE_URL + pathName
	
	except ClientError as e:
		logging.error(e)
		return False

	return url

def get_previous_orders_total_amount(retailer):
	total_amount = 0
	try:
		orders = Order.objects.filter(retailer=retailer).filter(Q(amount__gt=0)).filter(Q(pending_amount__gt=0))
		for order in orders:
			total_amount += order.amount
		return total_amount
	except:
		return total_amount

def add_order_items_to_order(retailer_obj, new_sales_order, order_items, sgst, cgst):
	sgst = 0
	cgst = 0
	grand_total = 0
	is_partial_order_successful = False
	output = {}
	failed_batch_items = []
	failed_commodity = []
	ordered_items = []
	total_other_charges = 0
	total_normal_product_price = 0

	for order_item in order_items:
		commodity_id = order_item['commodityId']
		commodity_obj = getComodityById(commodity_id)
		commodity_total_quantity = 0

		# if commodity_obj.available_quantity :
		# 	commodity_serializer = DcCommoditySerializer(commodity_obj)
		# 	failed_commodity.append(commodity_serializer.data)
		# 	for batch in order_item['batches']:
		# 		commodity_total_quantity += batch['qty']
		# 	dc = DistributionCenter.objects.get(id=1)
		# 	commodity_request = DistributionStoreIndent.objects.create(
		# 			dc=dc, 
		# 			dc_commodity=commodity_obj,
		# 			requested_qty=commodity_total_quantity
		# 	)
		for batch in order_item['batches']:
			commodity_batch_obj = getCommodityBatch(batch['id'])
			total_quantity_batch_price = batch['qty'] * commodity_batch_obj.price
			commodity_order_quantity = batch['qty']
			price = commodity_batch_obj.price

			order_item['orderItemTotal'] = total_quantity_batch_price
			order_item_price = commodity_batch_obj.price
			
			if commodity_batch_obj.available_quantity >= commodity_order_quantity:
				new_sales_order_item = OrderItem.objects.create(
						commodity=commodity_obj,
						commodity_batch=commodity_batch_obj,
						price=order_item_price,
						quantity=commodity_order_quantity
				)
				new_sales_order_item.delivery_charge = 0
				order_item_sgst = round((float(price * new_sales_order_item.quantity) * new_sales_order_item.commodity.commodity.gst/ 200), 4)
				order_item_cgst = round((float(price * new_sales_order_item.quantity) * new_sales_order_item.commodity.commodity.gst/ 200), 4)
				new_sales_order_item.sgst = order_item_sgst
				new_sales_order_item.cgst = order_item_cgst
				new_sales_order_item.save()
				sgst += new_sales_order_item.sgst
				cgst += new_sales_order_item.cgst
				total_other_charges += new_sales_order_item.sgst + new_sales_order_item.cgst
				total_normal_product_price += price * new_sales_order_item.quantity
				total_product_price = round(new_sales_order_item.price+(new_sales_order_item.price * (new_sales_order_item.commodity.commodity.gst / 100)), 2)
				order_item['orderItemTotal'] = (total_product_price * new_sales_order_item.quantity)
				grand_total += order_item['orderItemTotal']
				commodity_batch_obj.available_quantity -= commodity_order_quantity
				commodity_total_quantity += commodity_order_quantity
				commodity_batch_obj.save()
				# print("Grand total After Addition OF Commodity",grandTotal)
				new_sales_order.order_items.add(new_sales_order_item)
				new_sales_order.save()
				order_item_serializer = OrderItemSerializer(new_sales_order_item)
				order_item_data = order_item_serializer.data
				ordered_items.append(order_item_data)
			elif commodity_batch_obj.available_quantity < commodity_order_quantity:
				commodity_request = RetailerCommodityRequests.objects.create(
						retailer=retailer_obj,
						dc_commodity=commodity_obj
				)
				is_partial_order_successful = True
				new_sales_order_item = OrderItem.objects.create(
						commodity=commodity_obj, 
						price=order_item_price, 
						quantity=commodity_order_quantity, 
						status="Out_Of_Stock",
						commodity_batch=commodity_batch_obj
				)
				#Possible delivery charge change in future
				new_sales_order_item.delivery_charge = 0
				# order_item_sgst = round((float(price * new_sales_order_item.quantity) * new_sales_order_item.commodity.commodity.gst/ 200), 4)
				# order_item_cgst = round((float(price * new_sales_order_item.quantity) * new_sales_order_item.commodity.commodity.gst/ 200), 4)
				order_item_sgst = 0
				order_item_cgst = 0
				new_sales_order_item.sgst = order_item_sgst
				new_sales_order_item.cgst = order_item_cgst
				new_sales_order_item.save()

				sgst += new_sales_order_item.sgst
				cgst += new_sales_order_item.cgst
				total_product_price = round(new_sales_order_item.price + (new_sales_order_item.price * (new_sales_order_item.commodity.commodity.gst/100)),2)
				order_item['orderItemTotal'] = (total_product_price * new_sales_order_item.quantity)
				# Since Out Of Stock Do not Add Amount to Total
				# grandTotal +=orderItem['orderItemTotal']
				# print("Grand total After Addition OF Commodity",grandTotal)
				new_sales_order.order_items.add(new_sales_order_item)
				new_sales_order.save()
				failed_batch_items.append(jsonCommodityBatch(commodity_batch_obj))
				print("Creating a request for required commodities")
				dc = DistributionCenter.objects.get(id=1)
				commodity_request = DistributionStoreIndent.objects.create(
						dc=dc, 
						dc_commodity=commodity_obj,
						requested_qty=commodity_order_quantity
				)
			else:
				output['status'] = "failed"
				is_partial_order_successful = True
				failed_batch_items.append(jsonCommodityBatch(commodity_batch_obj))
				output['status_text'] = "Sorry " + "These commoditeies are " + " Out Of Stock!"
				# return HttpResponse(json.dumps(output))
		try:
			print("decreasing commodity available quantity..")
			commodity_obj.available_quantity -= commodity_total_quantity
			commodity_obj.save()
		except:
			pass

	if failed_batch_items:
		output["failed_batch_items"] = failed_batch_items
	
	if ordered_items:
		output["ordered_items"] = ordered_items
		output["total_other_charges"] = total_other_charges
		output["total_normal_product_charges"] = total_normal_product_price

	if failed_commodity:
		output["failed_commodity"] = failed_commodity
		output["status_msg2"] = "No batch available quantity for failed commodities, we will notify you when it arrives"

	return output, new_sales_order, grand_total, is_partial_order_successful


def get_total_credit(retailer_obj):
	try:
		amount = 0
		retailer_payments = RetailerPayment.objects.filter(retailer=retailer_obj)

		for payment in retailer_payments:
			amount += payment.amount
		
		return amount
	except:
		return 0

def get_order_data(order):
	grand_total = 0
	total_other_charges = 0
	total_normal_product_price = 0

	for order_item in order.order_items.all():
		if order_item.status != 'Out_Of_Stock':
			total_quantity_batch_price = order_item.quantity * order_item.commodity_batch.price
			# commodity_order_quantity = order_item.quantity
			price = order_item.commodity_batch.price

			order_item_total = total_quantity_batch_price
			
			order.delivery_charge = 0
			total_other_charges += order_item.sgst + order_item.cgst
			total_normal_product_price += price * order_item.quantity
			total_product_price = round(order_item.price+(order_item.price * (order_item.commodity.commodity.gst / 100)), 2)
			order_item_total = (total_product_price * order_item.quantity)
			grand_total += order_item_total
	
	return total_other_charges, grand_total, total_normal_product_price

def convert_string_to_number(string):
	split_num = string.split(",")
	join_split_num = "".join(split_num)
	num = float(join_split_num)
	return num

async def post_shipped_functions(order, notes):
	retailer = order.retailer
	try:
		message_desc = f"Your order has been shipped, {notes}"
	except:
		message_desc = f"Your order has been shipped."
	
	message_title = "MAHAVEER DRUG HOUSE: Order Shipped"
	title = "Order Shipped"
	notification_type = 'myorders'

	create_notification(retailer, message_desc, title, notification_type)

	asyncio.create_task(send_shipped_email(retailer, order, notes))
	asyncio.create_task(send_shipped_sms(retailer, order, notes))
	asyncio.create_task(send_browser_alert(retailer, message_desc, message_title))

async def post_delivered_functions(order):
	retailer = order.retailer

	message_desc = f"Your order has been delivered."
	
	message_title = "MAHAVEER DRUG HOUSE: Order Delivered"
	title = "Order Delivered"
	notification_type = 'myorders'

	create_notification(retailer, message_desc, title, notification_type)

	asyncio.create_task(send_delivered_email(retailer, order))
	asyncio.create_task(send_delivered_sms(retailer, order))
	asyncio.create_task(send_browser_alert(retailer, message_desc, message_title))

async def post_canceled_functions(order, notes):
	retailer = order.retailer
	try:
		message_desc = f"Your order has been canceled, {notes}"
	except:
		message_desc = f"Your order has been canceled."
	
	message_title = "MAHAVEER DRUG HOUSE: Order Canceled"
	title = "Order Canceled"
	notification_type = 'myorders'

	create_notification(retailer, message_desc, title, notification_type)

	asyncio.create_task(send_canceled_email(retailer, order, notes))
	asyncio.create_task(send_canceled_sms(retailer, order, notes))
	asyncio.create_task(send_browser_alert(retailer, message_desc, message_title))
