import json
import traceback, sys

from account.models import Retailer
from account.api.serializers.retailer_serializer import RetailerOrderSerializer
from account.decorators import is_retailer_manager

from rest_framework import status as Status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
@is_retailer_manager()
def set_is_payment_required_true(request):
    data = request.data
    output = {}
    
    try:
        retailer_id = data['retailerId']
        is_payment_required_true = data['isPaymentCheckRequired']
        try:
            retailer = Retailer.objects.get(id=retailer_id)
            try:
                Retailer.objects.filter(id=retailer_id).update(is_payment_check_required=is_payment_required_true)
                retailer_serializer = RetailerOrderSerializer(retailer)
                output['status'] = 'success'
                output['status_text'] = 'Successfully modified the Retailer'
                output['retailer'] = retailer_serializer.data
                status = Status.HTTP_200_OK
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Failed to modify the retailer configurations'
                status = Status.HTTP_304_NOT_MODIFIED
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'Retailer no found'
            status = Status.HTTP_404_NOT_FOUND
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'Invalid data'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)