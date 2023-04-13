import sys
import traceback

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from order.models import RetailerPayment, Order, OrderPayment
from order.api.serializers.retailer_payment import RetailerPaymentSerializer

from account.models import Retailer
from account.functions import add_amount_out_standing

@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def approveRetailerPayment(request):
	output = {}
	# data = json.loads(request.data)
	data = request.data
	
	try:
		retailer_payment_id = data['retailerPaymentId']
		
		try:
			retailer_payment = RetailerPayment.objects.get(id=retailer_payment_id)
			retailer = retailer_payment.retailer
			payment_mode = retailer_payment.payment_mode
			amount = retailer_payment.amount
		except ObjectDoesNotExist:
			output['status']="failed"
			output['status_text']="No matching retailer found"
			return Response(output, status=status.HTTP_400_BAD_REQUEST)
		
		try:
			retailer_payment.is_verified_by_admin = False
			retailer_payment.status = 'REFUND_GENERATED'
			retailer_payment.save()

			serializer = RetailerPaymentSerializer(retailer_payment)

			output['status'] = 'success'
			output['status_text'] = "Successfully created payment for retailer"
			output['retailer_payment'] = serializer.data
		except ObjectDoesNotExist:
			output['status'] = "failed"
			output['status_text'] = "failed to create the payment for retailer"
			return Response(output, status=status.HTTP_400_BAD_REQUEST)
	except KeyError as e:
		traceback.print_exc(file=sys.stdout)
		output['status'] = 'failed'
		output['status_text'] = f'{e}' + ": : Data is missing"
		return Response(output, status=status.HTTP_400_BAD_REQUEST)
	
	return Response(output, status=status.HTTP_200_OK)