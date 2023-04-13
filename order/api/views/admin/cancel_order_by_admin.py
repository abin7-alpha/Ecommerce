import traceback
import sys
import json
import asyncio

from rest_framework import status as Status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from order.models import Order
from order.api.serializers.order import OrderSerializer
from order.functions import post_canceled_functions

from account.functions import stock_available_send_notification

@api_view(['POST',])
@permission_classes([IsAuthenticated, ])
def cancel_order_admin(request):
    data = request.data
    output = {}

    try:
        order_id = data['orderId']
        dc_id = data['dcId']
        try:
            order = Order.objects.get(id=order_id)
            try:
                cancel_msg = data['cancellationMessage']
            except:
                cancel_msg = None
            try:
                order_items = order.order_items
                order.is_admin_verified = True
                for item in order_items.all():
                    commodity = item.commodity
                    commodity_batch = item.commodity_batch
                    quantity = item.quantity
                    commodity.available_quantity += quantity
                    commodity_batch.available_quantity += quantity
                    commodity.save()
                    commodity_batch.save()

                    if commodity.available_quantity > 0:
                        stock_available_send_notification(commodity)
                        
                order.status = 'Cancelled'
                order.save()

                asyncio.run(post_canceled_functions(order, cancel_msg))

                output['status'] = 'success'
                output['status_text'] = 'Successfully canceled the order'
                status = Status.HTTP_200_OK
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Failed to cancel the order'
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
            




