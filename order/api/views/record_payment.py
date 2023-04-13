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
def record_payment_for_retailer(request):
	output = {}
	# data = json.loads(request.data)
	data = request.data
	
	try:
		retailer_id = data['retailerId']
		amount = data['amount']
		txn_id = data['txnId']
		is_online_payment = data['isOnlinePayment']
		payment_mode = data['paymentMode']
		
		try:
			retailer = Retailer.objects.get(id=retailer_id)
		except ObjectDoesNotExist:
			output['status']="failed"
			output['status_text']="No matching retailer found"
			return Response(output, status=status.HTTP_400_BAD_REQUEST)
		
		try:
			retailer_payment = RetailerPayment.objects.create(
			        retailer=retailer, 
		            amount=amount,
		            status="APPROVAL_PENDING",
			    	txn_id=txn_id,
                    payment_mode=payment_mode,
                    is_online_payment=is_online_payment
            )
			
			serializer = RetailerPaymentSerializer(retailer_payment)
			
			output['status'] = 'success'
			output['status_text'] = "Successfully created payment for retailer"
			output['retailerPayments'] = serializer.data
			return Response(output, status=status.HTTP_200_OK)
		except:
			output['status'] = "failed"
			output['status_text'] = "failed to create the payment for retailer"
			return Response(output, status=status.HTTP_400_BAD_REQUEST)
	except KeyError as e:
		traceback.print_exc(file=sys.stdout)
		output['status'] = 'failed'
		output['status_text'] = f'{e}' + ": : Data is missing"
		return Response(output, status=status.HTTP_400_BAD_REQUEST)
	