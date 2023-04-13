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
def create_payment_for_order(request):
	output = {}
	# data = json.loads(request.data)
	data = request.data
	
	try:
		order_id = data['orderId']
		amount = data['amount']
		txn_id = data['txnId'] 
		try:
			order = Order.objects.get(id=order_id)
			retailer = order.retailer
			payment_mode = "Manual Entry"
			is_online_payment = False
		except:
			output['status']="failed"
			output['status_text']="Invalid Order"
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
			
			if order.pending_amount > amount:
				pending_amount = order.pending_amount - amount
				order_payment = OrderPayment.objects.create(
                    order=order,
                    retailer_payment=retailer_payment,
                    payment_type=payment_mode,
                    amount=amount,
		            is_verified_by_admin=True,
                    status='New'
                )
				order.pending_amount = pending_amount
				retailer = order.retailer
				retailer.total_amount_outstanding -= amount
				retailer.save()
				order.save()
				
			elif order.pending_amount < amount or order.pending_amount == amount:
				amount_outstanding = amount - order.pending_amount
				order_payment = OrderPayment.objects.create(
                    order=order,
                    retailer_payment=retailer_payment,
                    payment_type=payment_mode,
		            is_verified_by_admin=True,
                    amount=amount,
                    status='New'
                )
				order.pending_amount = 0
				retailer = order.retailer
				retailer.total_amount_outstanding -= amount_outstanding
				retailer.save()
				order.save()
			
			# serializer = RetailerPaymentSerializer(retailer_payment)
			
			output['status'] = 'success'
			output['status_text'] = "Successfully created payment for order"
			# output['retailerPayments'] = serializer.data
			return Response(output, status=status.HTTP_200_OK)
		except:
			output['status'] = "failed"
			output['status_text'] = "failed to create the payment for order"
			return Response(output, status=status.HTTP_400_BAD_REQUEST)
	except KeyError as e:
		traceback.print_exc(file=sys.stdout)
		output['status'] = 'failed'
		output['status_text'] = f'{e}' + ": : Data is missing"
		return Response(output, status=status.HTTP_400_BAD_REQUEST)
	