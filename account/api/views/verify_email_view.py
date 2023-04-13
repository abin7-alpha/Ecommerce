import json
import traceback
import sys

from account.models import BasicUser
from account.models import Retailer
from account.functions import decrpytUserVerificationToken

from django.core.exceptions import ObjectDoesNotExist
from django.core.signing import BadSignature, SignatureExpired

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status as Status

@api_view(['GET',])
@permission_classes([AllowAny])
def verify_user_email(request):
	output={}
	
	try:
		token = request.query_params['token']
		userjson = decrpytUserVerificationToken(token)

		try:
			user = BasicUser.objects.get(email=userjson['email'])
			is_email_verified = False
			try:
				# Removed User Active for email Verification
				retailer = Retailer.objects.get(user=user)
				if user.id==int(userjson['id']):
					is_email_verified=True
					user.is_active=True
					user.is_email_verified=True
					user.save()
					output['user_type']=user.user_type
			except ObjectDoesNotExist:
				print("No Retailer")
		except:
			users = BasicUser.objects.filter(email=userjson['email']).all()
			is_email_verified = False
			for user in users:
				try:
					# Removed User Active for email Verification
					retailer = Retailer.objects.get(user=user)
					if user.id == int(userjson['id']):
						is_email_verified = True
						user.is_active = True
						user.is_email_verified = True
						user.save()
						output['userType'] = user.userType
				except ObjectDoesNotExist:
					print("No Retailer")
		if is_email_verified:
			print("Email Verified Successfully")
			output['status'] = 'success'
			output['status_text'] = 'verification Success'
			status = Status.HTTP_200_OK
		else:
			raise BadSignature
	except SignatureExpired:
		traceback.print_exc(file=sys.stdout)
		output['status'] = "failed"
		output['error_code'] = 'Token_Expired'
		output['status_text'] = "Token Expired. Please Regenerate Verification Mail."
		status = Status.HTTP_408_REQUEST_TIMEOUT
	except BadSignature:
		traceback.print_exc(file=sys.stdout)
		output['status'] = "failed"
		output['error_code'] = 'Bad_Signature'
		output['status_text'] = "Email Verification Failed. Please Regenerate Verification Mail."
		status = Status.HTTP_400_BAD_REQUEST
	except ObjectDoesNotExist:
		traceback.print_exc(file=sys.stdout)
		output['status'] = "failed"
		output['error_code'] = 'Invalid_User'
		output['status_text'] = "Email Verification Failed Invalid Data."
		status = Status.HTTP_400_BAD_REQUEST
	except:
		traceback.print_exc(file=sys.stdout)
		output['status'] = "failed"
		output['status_text'] = "something went wrong please try again"
		status = Status.HTTP_400_BAD_REQUEST
	
	return Response(output, status=status)
