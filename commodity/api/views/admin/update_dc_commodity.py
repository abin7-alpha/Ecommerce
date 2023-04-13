import sys, traceback

from rest_framework import status as Status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from commodity.models import DcCommodity
from commodity.api.serializers.dc_commodity import DcCommodityForBatchSerializer

from office.models import DistributionCenter

from account.decorators import is_logistics_manager


@api_view(['POST',])
@permission_classes([IsAuthenticated, ])
@is_logistics_manager()
def update_dc_commodity(request):
    data = request.data
    print(data)
    output = {}

    try:
        dc_commodity_id = data['dcCommodityId']
        min_available_quantity = data['minimumAvailableQuantity']
        max_available_quantity = data['maximumAvailableQuantity']
        max_quantity_allowed_per_order = data['maximumQuantityAllowedPerOrder']
        # minimum_order_quantity = data['minimumOrderQuantity']

        distribution_center_id = None
        try:
            if type(data['dcId']) is dict:
                distribution_center_id = data['dcId']["id"]
            else:
                raise Exception
        except:
            distribution_center_id = data['dcId']

        try:
            distribution_center = DistributionCenter.objects.get(id=distribution_center_id)
            dc_commodity = DcCommodity.objects.get(id=dc_commodity_id)

            dc_commodity.distribution_center = distribution_center
            dc_commodity.min_available_qty = min_available_quantity
            dc_commodity.max_available_qty = max_available_quantity
            dc_commodity.max_qty_allowed_per_order = max_quantity_allowed_per_order
            # dc_commodity.minimum_order_quantity = minimum_order_quantity
            dc_commodity.save()

            # dc_commodities = DcCommodity.objects.filter(distribution_center=distribution_center).order_by('-updated')
            # dc_commodity_serializer = DcCommodityForBatchSerializer(dc_commodity)
            # dc_commodities_serializer = DcCommodityForBatchSerializer(dc_commodities, many=True)

            output['status'] = 'success'
            output['status_text'] = 'succesfully updated the Commodity'
            # output['updated_batch'] = dc_commodity_serializer.data
            # output['dcCommodities'] = dc_commodities_serializer.data
            status = Status.HTTP_200_OK
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'failed to update the Commodity'
            status = Status.HTTP_400_BAD_REQUEST
    
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = f'Key Error: {e}'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)
