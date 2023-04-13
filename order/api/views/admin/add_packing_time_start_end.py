import sys, traceback

from rest_framework import status as Status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from pytz import timezone
from datetime import datetime

from order.models import Order

@api_view(['POST',])
@permission_classes([IsAuthenticated, ])
def add_packing_data_for_order(request):
    data = request.data
    current_time = timezone('Asia/Kolkata').localize(datetime.now())
    output = {}

    try:
        order_id = data['orderId']
        order =Order.objects.get(id=order_id)
        try:
            if data['packingStartTime']:
                order.packed_start_time = current_time
                order.status = 'Packing_Started'
                order.updated = current_time
                order.save()
                output['status'] = 'success'
                output['status_text'] = 'succesfully Added packing start time'
                status = Status.HTTP_200_OK
            elif data['packingEndTime']:
                order.packed_end_time = current_time
                order.status = 'Packed'
                order.updated = current_time
                order.save()
                output['status'] = 'success'
                output['status_text'] = 'succesfully Added packing end time'
                status = Status.HTTP_200_OK
            else:
                raise Exception
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'failed to add packing data'
            status = Status.HTTP_400_BAD_REQUEST
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = f'Key Error: {e}'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)
