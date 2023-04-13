import asyncio

from crm.html_snippets import reply_email, reply_sms
from janaushadi import settings
from account.functions import send_mails, send_sms

from account.models import RetailerDevice
from account.functions import send_notification

async def send_browser_alert_ticket_reply(retailer, message):
	retailer_devices = RetailerDevice.objects.filter(retailer=retailer)
	to_lang = retailer.prefered_lang_code
	for device in retailer_devices:
		fcm_token = device.fcm_token
		message_desc = message
		message_title = "MAHAVEER DRUG HOUSE - Ticket Reply"
		send_notification(fcm_token, message_desc, message_title, to_lang)
		

async def send_reply_email(message, email):
	print("sending reply email")
	recipient = email
	app_name = settings.APP_NAME
	body_html = reply_email.substitute(
            message=message,
			app_name=app_name
	)

	subject = "Mahaveer Drug House: Service Request Reply"
    #   The Medicine <Name> you requested is available for purchase.
	body_text = (
		"Hi! This is Mahaveer Drug House\r\n"
	)
	value = send_mails(recipient, body_html, body_text, subject)
	return value

async def send_reply_sms(message, phone):
	retailer_phone = phone
	number = f'91{retailer_phone}'
	app_name = settings.APP_NAME
	msg = reply_sms.substitute(
            message=message,
			app_name=app_name
	)

	value = send_sms(msg, number)
	return value

async def send_reply(retailer, message, email, phone):
	print("im the one before")
	notifcation = asyncio.create_task(send_browser_alert_ticket_reply(retailer, message))
	reply_email = asyncio.create_task(send_reply_email(message, email))
	reply_sms =  asyncio.create_task(send_reply_sms(message, phone))
	print("im the one after")
	email =  await reply_email
	sms =  await reply_sms
