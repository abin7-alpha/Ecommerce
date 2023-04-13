import traceback
import sys

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.db.models import Q

from commodity.models import DcCommodity
from commodity.api.serializers.dc_commodity import DcCommodityForBatchSerializer

@api_view(['GET',])
@permission_classes([IsAuthenticated])
def check_commodity_availability_primary_dc(request):
    commodity_name = request.query_params['commodity_name']
    output = {}
    
    try:
        dc_commodity = DcCommodity.objects.filter(Q(available_quantity__gt=0)).filter(distribution_center__is_primary_dC=True).filter(commodity__name=commodity_name)
        
        serializer = DcCommodityForBatchSerializer(dc_commodity[0])
        output['status'] = 'available'
        output['status_txt'] = 'Commodity available in banglore dc'
        output['commodity_data'] = serializer.data
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'not_available'
        output['status_txt'] = 'No commodities available in banglore dc'
        return Response(output, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(output, status=status.HTTP_200_OK)
