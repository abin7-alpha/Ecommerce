import json
import traceback, sys

from account.models import Retailer
from account.decorators import is_retailer_manager
from account.api.serializers.retailer_serializer import RetailerOrderSerializer, RetailerSerializer

from office.models import DistributionCenter

from rest_framework import status as Status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST',])
@is_retailer_manager()
@permission_classes([IsAuthenticated,])
def assign_dc_for_retailer(request):
    data = request.data
    output = {}
    
    try:
        retailer_id = data['retailerId']
        dc_id = data["dcId"]

        try:
            retailer = Retailer.objects.get(id=retailer_id)
            distribution_center = DistributionCenter.objects.get(id=dc_id)
            try:
                retailer.dc = distribution_center
                retailer.save()

                retailer_serializer = RetailerOrderSerializer(retailer)
                retailers = Retailer.objects.all()
                retailers_serializer = RetailerSerializer(retailers, many=True)

                output['status'] = 'success'
                output['status_text'] = 'Successfully assigned distribution center for retailer'
                output['retailer'] = retailer_serializer.data
                output['retailers'] = retailers_serializer.data
                print(output['retailers'])
                status = Status.HTTP_200_OK
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Failed to assign distribution center for retailer'
                status = Status.HTTP_400_BAD_REQUEST
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'Retailer no found'
            status = Status.HTTP_400_BAD_REQUEST
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = f'Invalid data: Key error: {e}'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)