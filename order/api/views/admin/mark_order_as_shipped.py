import traceback
import sys
import asyncio

from pytz import timezone
from datetime import datetime

from rest_framework import status as Status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from order.models import Order, ShippingVendor, Notes
from order.api.serializers.order import OrderSerializer
from order.functions import post_shipped_functions

@api_view(['POST',])
@permission_classes([IsAuthenticated, ])
def mark_order_as_shipped(request):
    current_date = timezone('Asia/Kolkata').localize(datetime.now())
    data = request.data
    output = {}

    try:
        order_id = data['orderId']
        shipping_vendor_id = data['shipping_vendor']
        delivery_time = data['delivery_time']
        try:
            order = Order.objects.get(id=order_id)
            shipping_vendor = ShippingVendor.objects.get(id=shipping_vendor_id)
            try:
                
                try:
                    note_string = data['note']
                    note = Notes.objects.create(note=note_string)
                    order.notes.add(note)
                except:
                    note_string = None

                order.delivery_time = delivery_time
                order.status = 'Delivery_In_Progress'
                order.shipping_vendor = shipping_vendor
                order.shipped_time = current_date
                order.updated = current_date
                order.save()

                all_orders = Order.objects.all().order_by('-updated')
                all_orders_serializer = OrderSerializer(all_orders, many=True)

                asyncio.run(post_shipped_functions(order, note_string))

                output['status'] = 'success'
                output['status_text'] = 'successfully shipped the order'
                output['orders'] = all_orders_serializer.data
                status = Status.HTTP_200_OK
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Failed to ship the order'
                status = Status.HTTP_400_BAD_REQUEST
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'Invalid Order'
            status = Status.HTTP_400_BAD_REQUEST
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = f'Please Add the: {e}, '
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)
