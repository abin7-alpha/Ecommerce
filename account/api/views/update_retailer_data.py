import sys, traceback

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status as Status

from account.models import Retailer

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def update_user_data(request):
	output = {}
	data = request.data
	try:
		retailer_id = data['retailerId']
		user_name = data['userName']
		user_phone = data['userPhone']
		user_email = data['userEmail']
		try:
			retailer = Retailer.objects.get(id=retailer_id)
			try:
				basic_user = retailer.user
				basic_user.name = user_name
				basic_user.phone = user_phone
				basic_user.email = user_email
				basic_user.save()
				output['status'] = 'success'
				output['status_text'] = 'successfully updated the retailer data'
				status = Status.HTTP_200_OK
			except:
				traceback.print_exc(file=sys.stdout)
				output['status'] = 'failed'
				output['status_text'] = 'Failed to update the retailer data'
				status = Status.HTTP_304_NOT_MODIFIED
		except:
			traceback.print_exc(file=sys.stdout)
			output['status'] = 'failed'
			output['status_text'] = 'Invalid Retailer'
			status = Status.HTTP_404_NOT_FOUND
	except KeyError as e:
		traceback.print_exc(file=sys.stdout)
		output['status'] = 'failed'
		output['status_text'] = f'Invalid data,{e} key error'
		status = Status.HTTP_400_BAD_REQUEST
	
	return Response(output, status=status)