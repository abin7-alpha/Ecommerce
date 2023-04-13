import traceback
import sys
import json

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from order.models import Order
from order.api.serializers.order import OrderSerializerForDetails

@api_view(['POST',])
@permission_classes([IsAuthenticated])
def get_order_details(request):
    # data = json.loads(request.data)
    data = request.data
    order_id = data["orderId"]
    output = {}
    
    try:
        order = Order.objects.get(id=order_id)
        serializer = OrderSerializerForDetails(order)
        output['status'] = 'success'
        output['status_txt'] = 'Successfully fetched the details of order'
        output['order_details'] = serializer.data
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_txt'] = 'No order has found'
        return Response(output, status=status.HTTP_404_NOT_FOUND)
    
    return Response(output, status=status.HTTP_200_OK)
