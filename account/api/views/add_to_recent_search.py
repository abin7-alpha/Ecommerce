import traceback, sys

from account.models import Retailer, RetailerRecentSearch

from commodity.models import DcCommodity

from rest_framework import status as Status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def add_to_recent_searches(request):
    data = request.data
    output = {}
    
    try:
        retailer_id = data['retailerId']
        commodity_id = data['commodityId']
        try:
            retailer = Retailer.objects.get(id=retailer_id)
            commodity = DcCommodity.objects.get(id=commodity_id)
            try:
                RetailerRecentSearch.objects.create(
                    retailer=retailer,
                    dc_commodity=commodity
                )

                output['status'] = 'success'
                output['status_text'] = 'Successfully added commodity to recent searches'
                status = Status.HTTP_200_OK
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Failed to add commodity to recent searches'
                status = Status.HTTP_400_BAD_REQUEST
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'Retailer not found'
            status = Status.HTTP_400_BAD_REQUEST
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = f'Invalid data: Key error: {e}'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)