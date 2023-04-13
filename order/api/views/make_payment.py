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
def make_payments_for_retailer(request):
	output = {}
	# data = json.loads(request.data)
	data = request.data
	
	try:
		retailer_id = data['retailerId']
		amount = data['amount']
		txn_id = data['txnId']
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
		            status="INIT",
			    	txn_id=txn_id,
                    payment_mode=payment_mode,
		    )

			retailer_orders = Order.objects.filter(retailer=retailer).filter(Q(amount__gt=0)).filter(Q(pending_amount__gt=0)).order_by('created')

			payment = retailer_payment.amount
			balance_oustanding = 0
			if len(retailer_orders) != 0:
				for order in retailer_orders:
					if payment < 0 or payment == 0:
						break
					else:
						if order.pending_amount > payment:
							pending_amount = order.pending_amount - payment
							order_payment = OrderPayment.objects.create(
								order=order,
								retailer_payment=retailer_payment,
								payment_type=payment_mode,
								amount=payment,
								status='New'
							)

							order.pending_amount = pending_amount
							retailer = order.retailer
							retailer.total_amount_outstanding -= payment
							retailer.save()
							order.save()
							payment -= order_payment.amount
						elif order.pending_amount < payment or order.pending_amount == payment:
							amount_outstanding = payment - order.pending_amount
							order_payment = OrderPayment.objects.create(
								order=order,
								retailer_payment=retailer_payment,
								payment_type=payment_mode,
								amount=order.pending_amount,
								status='New'
							)

							order.pending_amount = 0
							retailer = order.retailer
							retailer.total_amount_outstanding -= amount_outstanding
							retailer.save()
							order.save()
							payment -= order_payment.amount
			else:
				retailer.total_amount_outstanding -= amount
				retailer.save()

			serializer = RetailerPaymentSerializer(retailer_payment)

			output['status'] = 'success'
			output['status_text'] = "Successfully created payment for retailer"
			output['retailerPayments'] = serializer.data
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