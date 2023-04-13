import traceback
import sys
import json

from rest_framework import status as Status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from order.models import Order, OrderPayment
from order.api.serializers.order_payment import OrderPaymentSerializer

from account.decorators import is_payment_manager

@api_view(['POST',])
@permission_classes([IsAuthenticated])
@is_payment_manager()
def get_all_order_payments(request):
    data = request.data
    output = {}

    try:
        order_id = data["orderId"]
        try:
            order = Order.objects.get(id=order_id)
            try:
                payments = OrderPayment.objects.filter(order=order)
                
                payment_serializer = OrderPaymentSerializer(payments, many=True)
                
                output['status'] = 'success'
                output['status_text'] = 'succesfully fetched the order payments'
                output['payments'] = payment_serializer.data
                status = Status.HTTP_200_OK
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Failed to fetch the order payments'
                status = Status.HTTP_400_BAD_REQUEST
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'Invalid Order'
            status = Status.HTTP_400_BAD_REQUEST
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = f'Key Error: {e}'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)

