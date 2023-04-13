import traceback
import sys

from rest_framework import status as Status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.db.models import Q

from order.models import Order
from order.api.serializers.order import OrderSerializerForDetails

from account.models import Retailer

@api_view(['POST',])
@permission_classes([IsAuthenticated])
def get_ledger_debit(request):
    data = request.data
    output = {}

    try:
        retailer_id = data['retailerId']
        try:
            retailer = Retailer.objects.get(id=retailer_id)
            try:
                retailer_orders = Order.objects.filter(retailer=retailer).order_by('-created').filter(Q(amount__gt=0))
                # retailer_debit = []
                # for order in retailer_orders:
                #     try:
                #         order_payment = OrderPayment.objects.filter(order=order)
                #         for payment in order_payment:
                #             order_payment_serializer = OrderPaymentSerializer(payment)
                #             retailer_debit.push(order_payment_serializer.data)
                #     except:
                #         continue
                order_serailizer = OrderSerializerForDetails(retailer_orders, many=True)

                output['status'] = 'success'
                output['status_text'] = 'Successfully Fetched all the retailer debits'
                output['reatiler_credits'] = order_serailizer.data
                status = Status.HTTP_200_OK
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Failed to fetch the retail debits'
                status = Status.HTTP_400_BAD_REQUEST
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'Retailer not found'
            status = Status.HTTP_400_BAD_REQUEST
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = f'Invalid data: {e}'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)
