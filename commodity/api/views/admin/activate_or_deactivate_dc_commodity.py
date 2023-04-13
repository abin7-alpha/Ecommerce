import sys, traceback

from pytz import timezone
from datetime import datetime

from rest_framework import status as Status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from commodity.models import DcCommodity
from commodity.api.serializers.dc_commodity import DcCommodityForBatchSerializer

from account.decorators import is_logistics_manager


@api_view(['POST',])
@permission_classes([IsAuthenticated, ])
@is_logistics_manager()
def activate_or_deactivate_dc_commodity(request):
    data = request.data
    current_time = timezone('Asia/Kolkata').localize(datetime.now())
    output = {}

    try:
        is_active = data['isActive']
        dc_commodity_id = data['dcCommodityId']
        try:
            dc_commodity = DcCommodity.objects.get(id=dc_commodity_id)
            dc_commodity.is_active = is_active
            dc_commodity.updated = current_time
            dc_commodity.save()

            # dc_commodities = DcCommodity.objects.all().order_by('-updated')
            # dc_commodity_serializer = DcCommodityForBatchSerializer(dc_commodities, many=True)

            output['status'] = 'success'
            output['status_text'] = 'succesfully updated the dcCommodity'
            # output['updated_dc_commodity'] = DcCommodityForBatchSerializer(dc_commodity).data
            # output['dcCommodities'] = dc_commodity_serializer.data
            status = Status.HTTP_200_OK
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'failed to update the dcCommodity'
            status = Status.HTTP_400_BAD_REQUEST
    
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = f'Key Error: {e}'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)
