import sys, traceback

from rest_framework import status as Status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from pytz import timezone
from datetime import datetime

from commodity.models import Commodity
from commodity.api.serializers.commodity import CommoditySerializer

from account.decorators import is_logistics_manager

@api_view(['POST',])
@permission_classes([IsAuthenticated, ])
@is_logistics_manager()
def activate_or_deactivate_commodity(request):
    data = request.data
    current_time = timezone('Asia/Kolkata').localize(datetime.now())
    output = {}

    try:
        is_active = data['isActive']
        commodity_id = data['commodityId']
        try:
            commodity = Commodity.objects.get(id=commodity_id)
            commodity.is_active = is_active
            commodity.updated = current_time
            commodity.save()

            # commodities = Commodity.objects.all().order_by('-updated')
            # commodity_serializer = CommoditySerializer(commodities, many=True)

            output['status'] = 'success'
            output['status_text'] = 'succesfully created the Commodity'
            # output['commodities'] = commodity_serializer.data
            status = Status.HTTP_200_OK
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'failed to create the Commodity'
            status = Status.HTTP_400_BAD_REQUEST
    
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = f'Key Error: {e}'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)
