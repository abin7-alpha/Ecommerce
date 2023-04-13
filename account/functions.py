import requests
import urllib
import json
import boto3
import traceback, sys
import asyncio

from googletrans import Translator

from pytz import timezone
from datetime import datetime, timedelta
from random import randint
from janaushadi import settings
from string import Template

from django.core import signing
from django.core.signing import TimestampSigner
from django.db.models import Q

from botocore.exceptions import ClientError

from account.html_snippets import user_verification_template, change_password_template, user_available_stocks_notification, commodity_availability_sms_template
from account.models import RetailerCommodityRequests, RetailerNotification, NotificationType, Retailer, RetailerDevice

from order.models import Order
from order.api.serializers.order import OrderSerializerForRecentOrder

signer=TimestampSigner(salt="extra")

def generate_OTP(phone):
	setOTP={}
	setOTP['phone']=phone
	setOTP['OTP']=randint(100000, 999999)
	return setOTP

def createUserVerificationToken(user):
	encrypetdUser = signing.dumps({"email": user.email,'id':str(user.id)},salt='wishaffair')
	value = signer.sign(encrypetdUser)
	token=value
	# print token
	# unsignedSessionValue=signer.unsign(value,max_age=20000)
	# print unsignedSessionValue
	# userJson=signing.loads(unsignedSessionValue)
	# print json.dumps(userJson)
	return token

def url_encode(word):
	new_word = urllib.parse.quote(word.encode('utf-8'), safe='')
	return new_word

def get_token(username, password, redirect_uri):
	output = {}
	url = f"{settings.TOKEN_SERVER_URL}/o/token/"

	client_info = f'client_id={settings.CLIENT_ID}&client_secret={settings.CLIENT_SECRET}&grant_type=password'
	redirect_uri = f'&redirect_uri={url_encode(redirect_uri)}'
	user_info = f'&username={url_encode(username)}&password={url_encode(password)}'
	payload = client_info + user_info + redirect_uri

	headers = {
		'Cache-Control': 'no-cache',
		'Content-Type': 'application/x-www-form-urlencoded',
	}

	response = requests.request("POST", url, headers=headers, data=payload)
	data = json.loads(response.text)
	# output["access_token"] = response["accesstoken"]
	# output["expires_in"] = response["expires_in"]

	return data

def decrpytUserVerificationToken(token):
	unsignedSessionValue=signer.unsign(token,max_age=20000)
	# unsignedSessionValue=token
	userJson=signing.loads(unsignedSessionValue,salt='wishaffair')
	# print ('json.dumps(userJson):',json.dumps(userJson))
	return userJson

def sendUserVerificationEmail(user_email, user):
	recipient = user.email
	# BODY_HTML = otpTemplateEmail.substitute(otpNumber=otp)
	user_name = user.name
	app_name = settings.APP_NAME
	domain_address = settings.DOMAIN_ADDRESS
	verification_token = createUserVerificationToken(user)

	body_html = user_verification_template.substitute(
			user_name=user_name, 
			app_name=app_name, 
			domain_address=domain_address, 
			verification_token=verification_token
	)
	
	subject = "Mahaveer Drug House : Verification"
    # The email body for recipients with non-HTML email clients.

	body_text = (
		"Hai! This is Mahaveer Drug House\r\n"
	)

	value = send_mails(recipient, body_html, body_text, subject)

	return value

async def send_commodity_avaibility_email(retailer, commodity, email, name):
	print("Mahaveer Drug House: Stock Available " + commodity.commodity.name)
	recipient = email
	user_name = name
	app_name = settings.APP_NAME
	body_html = user_available_stocks_notification.substitute(
			user_name=user_name,
			commodity_name = commodity.commodity.name,
			app_name=app_name
	)

	subject = "Mahaveer Drug House: Stock Available " + commodity.commodity.name
    #   The Medicine <Name> you requested is available for purchase.
	body_text = (
		"Hi! This is Mahaveer Drug House\r\n"
	)
	value = send_mails(recipient, body_html, body_text, subject)
	return value

async def send_commodity_avaibility_sms(retailer, commodity, phone, name):
	retailer_phone = phone
	number = f'91{retailer_phone}'
	user_name = name
	app_name = settings.APP_NAME
	msg = commodity_availability_sms_template.substitute(
			user_name=user_name,
			commodity_name = commodity.commodity.name,
			app_name=app_name
	)

	value = send_sms(msg, number)
	return value

async def create_retailer_notification(retailer, commodity):
	print("sending notification")
	title = "Stock available"
	subtitle = "Wear house updation"
	content = f"Stock is available for {commodity.commodity.name}, please order before it becomes unavailable"
	notification_type = NotificationType.objects.get(name='required-medicine')
	retailer_notification = RetailerNotification.objects.create(
			retailer=retailer,
			title=title,
			subtitle=subtitle,
			content=content,
			notification_type=notification_type
	)

	return retailer_notification

async def send_browser_alert_stock_available(retailer):
	retailer_devices = RetailerDevice.objects.filter(retailer=retailer)
	to_lang = retailer.prefered_lang_code
	for device in retailer_devices:
		fcm_token = device.fcm_token
		message_desc = "Your order has been approved by the admin"
		message_title = "MAHAVEER DRUG HOUSE-Order Approved"
		send_notification(fcm_token, message_desc, message_title, to_lang)

def create_retailer_commodity_req(retailer, commodity):
	request = RetailerCommodityRequests.objects.create(
		retailer=retailer,
		dc_commodity=commodity
	)

	return request

async def send_alerts(retailer, commodity, email, name, phone):
	print("im the one before")
	retailer_notification = asyncio.create_task(create_retailer_notification(retailer, commodity))
	response =  asyncio.create_task(send_commodity_avaibility_email(retailer, commodity, email, name))
	sms = asyncio.create_task(send_commodity_avaibility_sms(retailer, commodity, phone, name))
	print("im the one after")
	# notificaitions =  await retailer_notification
	# responses =  await response
	# await sms
	browser_alert = asyncio.create_task(send_browser_alert_stock_available(retailer))


def stock_available_send_notification(commodity):
	print(commodity.commodity.name)
	retailer_commodity_requests = RetailerCommodityRequests.objects.all()
	notification_sent_retailers = []
	for request in retailer_commodity_requests:
		retailer = request.retailer
		if commodity.id == request.dc_commodity.id:
			if request.no_of_times_notified >= settings.MAXIMUM_NOTIFICATIONS_FOR_COMMODITY_REQUESTS:
				request.is_deleted = True
				request.is_active = False
				request.save()
			else:
				request.no_of_times_notified += 1
				request.availabilty_last_notified = timezone('Asia/Kolkata').localize(datetime.now())
				request.save()
				email = retailer.user.email
				name = retailer.user.name
				phone = retailer.user.phone
				asyncio.run(send_alerts(retailer, commodity, email, name, phone))
				print("retailer appended functions started working")
				notification_sent_retailers.append(retailer)

	return notification_sent_retailers

def createAndSendChangePasswordRequest(userEmail,user):
	recipient = user.email
	# BODY_HTML = otpTemplateEmail.substitute(otpNumber=otp)
	user_name = user.name
	app_name = settings.APP_NAME
	domain_address = settings.DOMAIN_ADDRESS
	verification_token = createPasswordResetTokenEmail(user)

	body_html = change_password_template.substitute(
			user_name=user_name, 
			app_name=app_name, 
			domain_address=domain_address, 
			verification_token=verification_token
	)
	
	subject = "Mahaveer Drug House : Reset Password"
    # The email body for recipients with non-HTML email clients.

	body_text = (
		"Hai! This is Mahaveer Drug House\r\n"
	)

	value = send_mails(recipient, body_html, body_text, subject)

	return value, body_html

def createPasswordResetTokenEmail(user):
	encrypetdUser = signing.dumps({"email": user.email,'id':str(user.id)}, salt='humusresetpass')
	value = signer.sign(encrypetdUser)
	token=value
	return token

def decrpytUserpasswordResetTokenEmail(token):
	unsignedSessionValue=signer.unsign(token,max_age=3000)
	# unsignedSessionValue=token
	userJson=signing.loads(unsignedSessionValue,salt='humusresetpass')
	# print json.dumps(userJson)
	return userJson

def decrpytUserpasswordResetToken(token):
	unsignedSessionValue=signer.unsign(token,max_age=3000)
	# unsignedSessionValue=token
	userJson=signing.loads(unsignedSessionValue, salt='humusresetpass')
	# print json.dumps(userJson)
	return userJson

def send_sms(message, number):
    output = {}
    try:
        snsClient = boto3.client(
            'sns',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.SNS_REGION
        )
        response = snsClient.publish(
            Message=message,
            Subject="OTP",
            PhoneNumber=number
        )
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = "failed"
        output['status_text'] = format(e)
        output["message"] = "Excpetion"
        status = 400

    return output

# def send_mail_with_attachment(recipient, body_html, body_text, subject):	

def send_mails(recipient, body_html, body_text, subject):
    print("sending----email..")
    SENDER = settings.SENDER_EMAIL
    RECIPIENT = recipient
    SUBJECT = subject
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = body_text
    # The HTML body of the email.
    BODY_HTML = body_html
    CHARSET = "UTF-8"
    client = boto3.client(
        'ses',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.SNS_REGION
    )
    
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [RECIPIENT],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
	
    except ClientError as e:
        traceback.print_exc(file=sys.stdout)
        print("Error sending email")
        print(e.response['Error']['Message'])
        return 400
    else:
        traceback.print_exc(file=sys.stdout)
        print("Email sent! Message ID:"),
        print(response['MessageId'])
        return 200

def get_amount_out_standing(retailer):
	try:
		# amount_out_standing = 0
		# #greater than pending amount 0
		# orders = Order.objects.filter(retailer=retailer)
		# for order in orders:
		# 	amount_out_standing += order.pending_amount
		# return amount_out_standing
		amount_outstanding = retailer.total_amount_outstanding
		return amount_outstanding
	except:
		return 0

def get_yearly_till_date(retailer):
	try:
		annual_purchase = 0
		year = datetime.today().year
		if datetime.today().month<4:
			year = year-1
		sales_after = "01/" + "04" + "/" + str(year)
		current_date_time = timezone('Asia/Kolkata').localize(datetime.now())
		current_day = current_date_time.day + 1
		current_month = current_date_time.month
		current_year = current_date_time.year
		sales_before = F"{str(current_day)}/{str(current_month)}/{str(current_year)}"
		datetime_start = datetime.strptime(sales_after, "%d/%m/%Y")
		datetime_end = datetime.strptime(sales_before, "%d/%m/%Y") + timedelta(hours=23, minutes=59, seconds=59)
		orders = Order.objects.filter(retailer=retailer).filter(created__gte=datetime_start, created__lte=datetime_end)
		for order in orders:
			annual_purchase += order.amount
		return annual_purchase
	except:
		return 0

def get_monthly_till_date(retailer):
	try:
		monthly_purchase = 0
		current_date_time = timezone('Asia/Kolkata').localize(datetime.now())
		current_day = current_date_time.day + 1
		current_month = current_date_time.month
		current_year = current_date_time.year
		sales_after = "01/" + str(current_month) + "/" + str(current_year)
		current_date_time = timezone('Asia/Kolkata').localize(datetime.now())
		sales_before = F"{str(current_day)}/{str(current_month)}/{str(current_year)}"
		datetime_start = datetime.strptime(sales_after, "%d/%m/%Y")
		datetime_end = datetime.strptime(sales_before, "%d/%m/%Y") + timedelta(hours=23, minutes=59, seconds=59)
		orders = Order.objects.filter(retailer=retailer).filter(created__gte=datetime_start, created__lte=datetime_end)
		# current_month = current_date_time.month
		# current_year = current_date_time.year
		# orders = Order.objects.filter(retailer=retailer).filter(created__year=current_year).filter(created__month=current_month)
		for order in orders:
			monthly_purchase += order.amount
		return monthly_purchase
	except:
		return 0

def get_last_sales(retailer):
	try:
		orders = Order.objects.filter(retailer=retailer)
		return len(orders)
	except:
		return 0

def get_recent_order(retailer):
	try:
		orders = Order.objects.filter(retailer=retailer).order_by('-created')
		recent_order = orders[0]
		total_products = recent_order.get_total_products
		order_serializer = OrderSerializerForRecentOrder(orders[0])
		data = order_serializer.data
		data.update({"total_items": total_products})
		return data
	except:
		return None
	
def add_amount_out_standing():
	for retailer in Retailer.objects.all():
		try:
			amount_out_standing = 0
			#greater than pending amount 0
			orders = Order.objects.filter(retailer=retailer)
			for order in orders:
				amount_out_standing += order.pending_amount
			retailer.total_amount_outstanding = amount_out_standing
			retailer.save()	
		except:
			retailer.total_amount_outstanding = 0
			retailer.save()

def out_standing_above_thirty_days(retailer):
	current_date_time = timezone('Asia/Kolkata').localize(datetime.now()) + timedelta(1)
	end_date_time = timezone('Asia/Kolkata').localize(datetime.now()) - timedelta(30)
	try:
		orders = Order.objects.filter(retailer=retailer).filter(~Q(created__gte=end_date_time, created__lte=current_date_time))
		amount_outstanding = 0
		print("amount_oustanding", amount_outstanding)
		for order in orders:
			print(order.created)
			amount_outstanding += order.pending_amount
			print("amount_oustanding", amount_outstanding)
		return amount_outstanding
	except:
		amount_outstanding = 0
		return amount_outstanding

def send_notification(fcm_token, message_desc, message_title, to_lang):
    # fcm_token = 'f9IWKqSSyQC4ZmTDaUn3cN:APA91bE379Uqkh_cJnc7brdlux7NnyEy6_UL8ttkn0MbgOksxxMa7SO9hxGY0nlzoS9eWg8m3ihDndT28fF6JndOtizsE7vYsOYQaG_0-KcxfqdEB6K_f5MLWHOmdFsSaNoI55lFwLTK'
    print("browser alert--------------coming")
    serverKey = settings.SERVER_KEY
    url = "https://fcm.googleapis.com/fcm/send"

    headers = {
        "Content-Type": "application/json",
        "Authorization": 'key='+ serverKey
	}
    translator = Translator()
    from_lang = 'en'
    print(to_lang, "tolang")
    translated_message = translator.translate(message_desc, dest=to_lang)
    print(translated_message.text)
    payload = 	{
		"notification": {
			"title": message_title,
			"text": " ",
			"body": translated_message.text
		},
		"to": fcm_token
	}
    try:
        result = requests.post(url,  data=json.dumps(payload), headers=headers)
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
