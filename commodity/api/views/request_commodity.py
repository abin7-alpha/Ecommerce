import traceback
import sys

from janaushadi import settings

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from commodity.models import DcCommodity
from account.models import RetailerCommodityRequests, Retailer

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def request_commodity(request):
    # data = json.loads(request.data)
    data = request.data

    try:
        retailer_id = data['retailerId']
        dc_commodity_id = data['dcCommodityId']

        output = {}
        
        failed_status = 'failed'
        success_status = 'success'
        try:
            retailer = Retailer.objects.get(id=retailer_id)
            dc_commodity = DcCommodity.objects.get(id=dc_commodity_id)

            try:
                previous_exist = RetailerCommodityRequests.objects.filter(retailer=retailer).get(dc_commodity=dc_commodity)
                output['status'] = 'previous_request_exists'
                output['status_txt'] = 'Request for this commodity already exists'
            except:
                try:
                    retailer_commodity_request = RetailerCommodityRequests.objects.create(
                            retailer=retailer,
                            dc_commodity = dc_commodity,
                            is_active = True,
                    )

                    output['status'] = success_status
                    output['status_txt'] = 'Successfully requested the commodity'
                    output['request_id'] = retailer_commodity_request.id
                except:
                    traceback.print_exc(file=sys.stdout)
                    output['status'] = failed_status
                    output['status_txt'] = 'Failed to request the commodity'
                    return Response(output, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_txt'] = 'No distribution center or distribution center commodity found'
            return Response(output, status=status.HTTP_404_NOT_FOUND)
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_txt'] = 'Check the validity of credentials ad try again'
        return Response(output, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(output, status=status.HTTP_200_OK)
