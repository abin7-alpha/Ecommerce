import json
import sys
import traceback

from janaushadi import settings

from geoposition import Geoposition

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from account.models import BasicUser, Retailer, RetailerShop
from account.functions import generate_OTP, sendUserVerificationEmail
from account.api.serializers.retailer_serializer import RetailerSerializer
from account.decorators import is_retailer_manager

from office.models import DistributionCenter

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site


@api_view(['POST',])
@permission_classes([AllowAny,])
@is_retailer_manager()
def register_retailer_by_admin(request):
	# data = json.loads(request.data)
	data = request.data
	output = {}
	try:
		name = data['userName']
		phone = data['userPhone']
		password = data['password']
		shop_name = data['shopName']
		user_type = 'Retailer'
		
		try:
			shop_pic_in = data['shop_pic_in']
		except:
			shop_pic_in = None
			
		try:
			shop_pic_out = data['shop_pic_out']
		except:
			shop_pic_out = None
			
		try:
			shop_position = data['shop_position']
		except:
			print("No Shop Position")
			shop_position = None
			
		try:
			email = data['userEmail']
			django_user_email = email
		except:
			email = None

		try:
			dc_id = data['dcId']
			dc = DistributionCenter.objects.get(id=dc_id)
		except:
			dc = None

		try:
			pending_amount_limit = data['pendingAmountLimit']
		except:
			pending_amount_limit = None

		if email!=None:
			if len(email)==0:
				email=None
		
		# django_user_email = str(phone) + settings.RETAILER_CLIENT_DOMAIN
		# django_user_name = str(phone) + settings.RETAILER_CLIENT_DOMAIN
		django_user_email = str(email)
		django_user_name = str(email)
		# print ("userType: ",userType)
		try:
			# print(userEmail)
			django_user = User.objects.create_user(
			    django_user_name, email=django_user_email ,password=password
		    )
			# django_user.save()
		except IntegrityError:
			try:
				django_user = User.objects.get(username=django_user_name)
			except ObjectDoesNotExist:
				try:
					django_user = User.objects.get(email=django_user_email)
				except ObjectDoesNotExist:
					output['status'] =' failed'
					output['status_text'] = 'Unknown error! '
			try:
				user = BasicUser.objects.get(django_user=django_user)
			except ObjectDoesNotExist:
				print("Nomatching basic User For Django User")


		except:
			# django_user=User.objects.get(email=userEmail)

			traceback.print_exc(file=sys.stdout)
			output["status"] = "userexist"
			output["status_text"] = "You are already a "+settings.APP_NAME+" registered retailer please login."
			return Response(json.dumps(output), status=status.HTTP_400_BAD_REQUEST)
		try:
			user = BasicUser.objects.create(
			        name=name , email=email ,phone=phone, passcode=password, 
		            user_type=user_type, django_user=django_user
		    )
			
			user.is_active = True
			try:
				secondary_contact_num = data['secondaryPhone']
				user.secondaryPhone = secondary_contact_num
				user.save()
			except:
				secondary_contact_num = None
				
			# output['user']=getJsonOfBasicUserObject(user)
			current_site = get_current_site(request).domain
			
			# userEmail=user.email
			# if userEmail!=None:
			# 	sendUserVerificationEmail(userEmail, user)
				
			retailer=Retailer.objects.create(user=user)
			# retailer.isPaymentCheckRequired=True
			retailer.is_payment_check_required = False
			retailer.is_admin_verified = True
			if dc:
				retailer.dc = dc
			if pending_amount_limit:
				retailer.pending_amount_limit = pending_amount_limit
			retailerShopObj = RetailerShop.objects.create(shop_name=shop_name)
			retailer.shops.add(retailerShopObj)
			retailer.shop_pic_in = shop_pic_in
			retailer.shop_pic_out = shop_pic_out
			retailerShopObj.shop_pic_in = shop_pic_in
			retailerShopObj.shop_pic_out = shop_pic_out
			
			if shop_position!=None:
				print(json.dumps(shop_position))
				try:
					# print(shop_position['latitude'])
					latitude=shop_position['latitude']
					longitude=shop_position['longitude']
					retailer.position=Geoposition(latitude,longitude)
					retailerShopObj.position=Geoposition(latitude,longitude)
				except:
					traceback.print_exc(file=sys.stdout)
					print("No Latiude")
					print("No longitude")
				# retailer.position.longitude=Decimal(positionJson['longitude'])
					
			retailer.save()
			retailerShopObj.save()
			
			retailer_serializer = RetailerSerializer(retailer)
			
			OTP=generate_OTP(user.phone)
			user.otp=OTP['OTP']
			user.save()
			
			try:
				print("OTP: ",user.otp)
				otpmsg="Your Humus App 6 Digit login OTP  : "+str(user.otp)
				# Removing SMS here Since Generate OTP is called in App flow post register
				# send_transactional_sms(user.phone,otpmsg)
				# send_transactional_sms_msg91(retailer.user.phone,otpmsg)
				# if user.email!=None:
				# 	sendUserLoginOTPMail(user,user.OTP)
			except Exception as e:
				traceback.print_exc(file=sys.stdout)
				print('failed to send otp')

			# otpmsg="Your Humus App 6 Digit login OTP  : "+str(basicUser.OTP)
			# send_transactional_sms_msg91(retailer.user.phone,otpmsg)
			# sendNewRetailerRequestNotificationMailToAdmin(retailer)
			
			output['user'] = retailer_serializer.data
			output['status']="success"
			output['status_text']="Successfully Registered"
		except IntegrityError:
			traceback.print_exc(file=sys.stdout)
			if email!=None:
				try:
					django_user=User.objects.get(email=email)
					django_user.delete()
				except:
					output['status']="failed"
					output['status_text']="Contact Number Or Email. Already registered."
					return Response(output, status=status.HTTP_400_BAD_REQUEST)
			output['status']="failed"
			output['status_text']="Contact Number Or Email. Already registered."
			return Response(output, status=status.HTTP_400_BAD_REQUEST)
		except:
			traceback.print_exc(file=sys.stdout)
			if email!=None:
				django_user=User.objects.get(email=email)
				django_user.delete()
			output['status']="failed"
			output['status_text']="Failed To register. Please Try Again!"
			return Response(output, status=status.HTTP_400_BAD_REQUEST)
		
	except KeyError as e:
		traceback.print_exc(file=sys.stdout)
		output['status']="Failed"
		output['status_text']="Failed to Create User. Key Error "+format(e)+" Not Specified"
	except:
		traceback.print_exc(file=sys.stdout)
		output['status']="Failed"
		output['status_text']="Failed to Create User"
		
	return Response(output, status=status.HTTP_200_OK)
