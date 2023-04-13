import traceback
import sys
import json

from rest_framework import status as Status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from order.models import RetailerPayment
from order.api.serializers.retailer_payment import AllRetailerPaymentSerializer

from account.decorators import is_payment_manager

@api_view(['GET',])
@permission_classes([IsAuthenticated])
@is_payment_manager()
def get_all_retailer_payments(request):
    output = {}

    try:
        retailer_payments = RetailerPayment.objects.all().order_by('-created')
        try:
            
            retailer_payment_serializer = AllRetailerPaymentSerializer(retailer_payments, many=True)
            
            output['status'] = 'success'
            output['status_text'] = 'succesfully fetched the retailer payments'
            output['retailer_payments'] = retailer_payment_serializer.data
            status = Status.HTTP_200_OK
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'Failed to fetch the retailer payments'
            status = Status.HTTP_400_BAD_REQUEST
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'Invalid Order'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)