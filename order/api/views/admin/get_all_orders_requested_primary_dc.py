import sys, traceback

from django.db.models import Q

from rest_framework import status as Status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from order.models import Order
from order.api.serializers.order import OrderSerializerForDetails

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_orders(request):
    output = {}
    dc_id = request.query_params.get('dcId')

    try:
        # all_orders = Order.objects.filter(Q(amount__gt=0)).filter(Q(pending_amount__gt=0))
        all_orders = Order.objects.filter(retailer__dc__is_primary_dC=False).order_by('-created')
        all_orders_serializer = OrderSerializerForDetails(all_orders, many=True)
        output['status'] = 'success'
        output['status_text'] = 'successfully fetched all the orders'
        output['orders'] = all_orders_serializer.data
        status = Status.HTTP_200_OK
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'failed to fetch the orders'
        status = Status.HTTP_404_NOT_FOUND

    return Response(output, status=status)