import sys, traceback

from rest_framework import status as Status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from commodity.models import DcCommodity, Commodity
from commodity.api.serializers.dc_commodity import DcCommoditySerializer, DcCommodityForBatchSerializer

from office.models import DistributionCenter

from account.decorators import is_logistics_manager


@api_view(['POST',])
@permission_classes([IsAuthenticated, ])
@is_logistics_manager()
def create_dc_commodity(request):
    data = request.data
    output = {}

    try:
        # dc_commodity_id = data['dcCommodityId']
        commodity_id = data['commodityId']
        is_janaushadi = data['isJanaushadi']
        min_available_quantity = data['minimumAvailableQuantity']
        max_available_quantity = data['maximumAvailableQuantity']
        max_quantity_allowed_per_order = data['maximumQuantityAllowedPerOrder']
        minimum_order_quantity = data['minimumOrderQuantity']

        distribution_center_id = None
        try:
            if type(data['dcId']) is dict:
                distribution_center_id = data['dcId']["id"]
            else:
                raise Exception
        except:
            distribution_center_id = data['dcId']

        try:
            commodity = Commodity.objects.get(id=commodity_id)
            distribution_center = DistributionCenter.objects.get(id=distribution_center_id)
            dc_commodity = DcCommodity.objects.create(
                commodity=commodity,
                distribution_center=distribution_center,
                available_quantity=0,
                min_available_qty=min_available_quantity,
                max_available_qty=max_available_quantity,
                max_qty_allowed_per_order=max_quantity_allowed_per_order,
                minimum_order_quantity=minimum_order_quantity,
                is_janaushadi=is_janaushadi
            )

            # dc_commodities = DcCommodity.objects.filter(distribution_center=distribution_center)
            # dc_commodity_serializer = DcCommoditySerializer(dc_commodity)
            # dc_commodities_serializer = DcCommodityForBatchSerializer(dc_commodities, many=True)

            output['status'] = 'success'
            output['status_text'] = 'succesfully created the dc Commodity'
            # output['updated_batch'] = dc_commodity_serializer.data
            # output['dcCommodities'] = dc_commodities_serializer.data
            status = Status.HTTP_200_OK
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'failed to create the dc Commodity'
            status = Status.HTTP_400_BAD_REQUEST
    
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = f'Key Error: {e}'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)
