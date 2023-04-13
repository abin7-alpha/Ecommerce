import traceback
import sys
import asyncio

from pytz import timezone
from datetime import datetime

from rest_framework import status as Status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from order.models import Order
from order.api.serializers.order import OrderSerializer
from order.functions import post_delivered_functions

@api_view(['POST',])
@permission_classes([IsAuthenticated, ])
def mark_order_as_delivered(request):
    current_date = timezone('Asia/Kolkata').localize(datetime.now())
    data = request.data
    output = {}

    try:
        order_id = data['orderId']
        try:
            order = Order.objects.get(id=order_id)
            try:
                order.status = 'Delivered'
                order.delivery_time = current_date
                order.updated = current_date
                order.save()

                all_orders = Order.objects.all().order_by('-updated')
                all_orders_serializer = OrderSerializer(all_orders, many=True)

                asyncio.run(post_delivered_functions(order))

                output['status'] = 'success'
                output['status_text'] = 'successfully cofirm the order'
                output['orders'] = all_orders_serializer.data
                status = Status.HTTP_200_OK
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Failed to confirm the order'
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
