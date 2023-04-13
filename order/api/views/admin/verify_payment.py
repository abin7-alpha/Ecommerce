import traceback
import sys
import json

from rest_framework import status as Status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from order.models import OrderPayment, Order
from order.api.serializers.order import OrderSerializer

from janaushadi import settings

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def verify_order_payment(request):
    data = request.data
    output = {}

    try:
        payment_id = data['paymentId']
        try:
            payment = OrderPayment.objects.get(id=payment_id)
            try:
                payment.status = 'ADMIN_VERIFIED'
                payment.is_verified_by_admin = True
                payment.save()

                all_orders = Order.objects.all()
                all_orders_serializer = OrderSerializer(all_orders, many=True)

                output['status'] = 'success'
                output['status_text'] = 'successfully verified the payment'
                output['orders'] = all_orders_serializer.data
                status = Status.HTTP_200_OK
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Failed to verify payment'
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
