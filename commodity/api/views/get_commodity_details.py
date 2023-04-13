import traceback
import sys

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from commodity.models import DcCommodity
from commodity.api.serializers.dc_commodity import DcCommoditySerializer

@api_view(['GET',])
@permission_classes([IsAuthenticated])
def get_commodity_details(request):
    batch_id = request.query_params['commodity_id']
    output = {}
    
    try:
        dc_commodity_batch = DcCommodity.objects.get(id=batch_id)
        serializer = DcCommoditySerializer(dc_commodity_batch)
        output['status'] = 'success'
        output['status_txt'] = 'Successfully fetched the details of commodity'
        output['commodity_data'] = serializer.data
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_txt'] = 'No commodity has found'
        return Response(output, status=status.HTTP_404_NOT_FOUND)
    
    return Response(output, status=status.HTTP_200_OK)
