import sys
import traceback
import json

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status as Status

from django.views.decorators.csrf import csrf_exempt
from django.core.signing import SignatureExpired, BadSignature
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from account.models import BasicUser
from account.functions import createAndSendChangePasswordRequest, decrpytUserpasswordResetTokenEmail
from account.functions import decrpytUserpasswordResetToken

from django.core.exceptions import ObjectDoesNotExist

@api_view(['POST',])
@permission_classes([AllowAny, ])
@csrf_exempt
def request_new_password(request):
	output = {}
	data = request.data
	try:
		userEmail = data['userEmail']

		django_user = User.objects.get(email=userEmail)
		user = BasicUser.objects.get(django_user=django_user)
		
		createAndSendChangePasswordRequest(userEmail,user)
		
		output['status'] = "success"
		output['status_text'] = "Reset Password link sent to your registered email!"
		status = Status.HTTP_200_OK
	except (ObjectDoesNotExist) as e:
		output['status'] = "failed"
		output['error_code'] = 'Invalid_User'
		output['status_text'] = 'We do not remember to have registered you before. Please contact Admin.'
		status = Status.HTTP_401_UNAUTHORIZED
	except (Exception) as e:
		traceback.print_exc(file=sys.stdout)
		output['status'] = "failed"
		output['status_text'] = format(e)
		status = Status.HTTP_400_BAD_REQUEST

	return Response(output, status=status)

@csrf_exempt
@api_view(['POST',])
@permission_classes([AllowAny, ])
def reset_password_request(request):
	output = {}
	data = request.data
	try:
		token = data['token']
		userjson = decrpytUserpasswordResetTokenEmail(token)
		user = BasicUser.objects.get(email=userjson['email'])
		if user.id == int(userjson['id']):
			output['status'] = "success"
			output['token'] = token
		else:
			raise BadSignature
		output['status'] = 'success'
		output['status_text'] = 'valid reset'
	except BadSignature:
		output['status'] = "failed"
		output['error_code'] = 'Bad_Signature'
		output['status_text'] = "Email Verification Failed. Please Regenerate Verification Mail."
	except ObjectDoesNotExist:
		output['status'] = "failed"
		output['error_code'] = 'Invalid_User'
		output['status_text'] = "Email Verification Failed Invalid Data."
	except:
		traceback.print_exc(file=sys.stdout)
		output['status'] = "failed"
		output['status_text'] = "something went wrong please try again"
	return Response(json.dumps(output))

@csrf_exempt
@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def change_user_password_console(request):
	output = {}
	# data = json.loads(request.data)
	data = request.data
	try:
		old_password = data['oldPassword']
		new_password = data['newPassword']
		user_name = data['userName']
		try:
			django_user = User.objects.get(username=user_name)
			user = authenticate(username=user_name, password=old_password)
			try:
				if user is not None:
					basic_user = BasicUser.objects.get(django_user=django_user)
					django_user.set_password(new_password)
					django_user.save()
					basic_user.passcode = new_password
					basic_user.save()
					output['status'] = "success"
					output['status_text'] = "Successfully Updated Your New Password"
					status = Status.HTTP_200_OK	
				else:
					raise Exception
			except:
				output['status'] = "failed"
				output['status_text'] = "Not matching with old password"
				status = Status.HTTP_401_UNAUTHORIZED
		except ObjectDoesNotExist:
			traceback.print_exc(file=sys.stdout)
			output['status'] = "failed"
			output['statusError'] = "invalidUser"
			output['status_text'] = "User Not Registered With this Mail"
			status = Status.HTTP_401_UNAUTHORIZED
	except KeyError as e:
		traceback.print_exc(file=sys.stdout)
		output['status'] = "failed"
		output['status_text'] = f'key error: {str(e)}'
		status = Status.HTTP_400_BAD_REQUEST
	return Response(output, )

@api_view(['POST',])
@permission_classes([AllowAny,])
def change_user_password_forgot(request):
	output = {}
	# data = json.loads(request.data)
	data = request.data
	try:
		newPassword = data['newPassword']
		email = data['userEmail']

		basic_user = BasicUser.objects.get(email=email)
		django_user = basic_user.django_user
		django_user.set_password(newPassword)
		django_user.save()
		basic_user.passcode = newPassword
		basic_user.save()
		output['status'] = "success"
		output['status_text'] = "Successfully Updated Your New Password"
		status = Status.HTTP_200_OK		

	except BadSignature:
		traceback.print_exc(file=sys.stdout)
		output['status'] = "failed"
		output['error_code'] = 'Bad_Signature'
		output['status_text'] = "Validation Failed. Please Regenerate Password Reset Request."
		status = Status.HTTP_400_BAD_REQUEST
	except ObjectDoesNotExist:
		traceback.print_exc(file=sys.stdout)
		output['status'] = "failed"
		output['statusError'] = "invalidUser"
		output['status_text'] = "User Not Registered With this Mail"
		status = Status.HTTP_401_UNAUTHORIZED
	except KeyError as e:
		traceback.print_exc(file=sys.stdout)
		output['status'] = "failed"
		output['status_text'] = f'key error: {str(e)}'
		status = Status.HTTP_400_BAD_REQUEST
	return Response(output,status=status)
