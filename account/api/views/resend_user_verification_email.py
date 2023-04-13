import traceback
import sys
import json

from account.models import BasicUser, Retailer
from account.functions import sendUserVerificationEmail

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST',])
@permission_classes([AllowAny,])
def resend_user_verification_mail(request):
	# data = json.loads(request.data)
	data = request.data
	output = {}
	try:
		email = data['email']
		try:
			user = BasicUser.objects.get(email=email)
			try:
				# Removed is Active for get Retailer
				retailer = Retailer.objects.get(user=user)
				sendUserVerificationEmail(user.email,user)
			except ObjectDoesNotExist:
				print("No Retailer")
		except:
			users = BasicUser.objects.filter(email=email).all()
			for user in users:
				try:
					retailer=Retailer.objects.get(user=user)
					sendUserVerificationEmail(user.email,user)
				except ObjectDoesNotExist:
					print("No Retailer")
		output['status']='success'
		output['status_text']='verification LInk send to your Registerd Email'
	except ObjectDoesNotExist:
		output['status']='failed'
		output['status_text']="No Matching user"
		return Response(json.dumps(output), status=status.HTTP_404_NOT_FOUND)
	except:
		traceback.print_exc(file=sys.stdout)
		output['status']="failed"
		output['status_text']="something went wrong please try again"
	
	return Response(json.dumps(output))
