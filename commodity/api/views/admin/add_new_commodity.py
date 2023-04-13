import sys, traceback

from rest_framework import status as Status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from commodity.models import Commodity, DcCommodity, CommodityMeasuringUnits, CommodityCategory, CommodityGroup, DrugManufacturer
from commodity.api.serializers.commodity import CommoditySerializer

from office.models import DistributionCenter

from account.decorators import is_logistics_manager


@api_view(['POST',])
@permission_classes([IsAuthenticated, ])
@is_logistics_manager()
def add_new_commodity(request):
    data = request.data
    output = {}

    try:
        measuring_unit = data['measuringUnit']
        commodity_category = data['commodityCategory']
        commodity_group = data['commodityGroup']
        drug_manufacturer = data['drugManufacturer']
        name = data['name']
        # max_available_qty = data['maximumAvailableQuantity']
        # min_available_qty = data['minimumAvailableQuantity']
        # max_qty_allowed_per_order = data['maximumQuantityAllowedPerOrder']
        # minimum_order_quantity = data['minimumOrderQuantity']
        salt_name = data['saltName']
        mm_code = data['mmCode']
        # dc_id = data['dcId']

        try:
            gst = data['gst']
        except:
            gst = 0.0

        try:
            hsn_code = data['hsnCode']
        except:
            hsn_code = ""

        try:
            mtm_name = data['mtmName']
        except:
            mtm_name = ""

        try:
            measuring_unit_obj = CommodityMeasuringUnits.objects.get(id=measuring_unit)
            commodity_category_obj = CommodityCategory.objects.get(id=commodity_category)
            commodity_group_obj = CommodityGroup.objects.get(id=commodity_group)
            drug_manufacturer_obj = DrugManufacturer.objects.get(id=drug_manufacturer)
            commodity = Commodity.objects.create(
                name=name,
                salt_name=salt_name,
                mm_code=mm_code,
                hsncode=hsn_code,
                searchkey=salt_name,
                mtm_name=mtm_name,
                measuring_unit=measuring_unit_obj,
                commodity_category=commodity_category_obj,
                commodity_group=commodity_group_obj,
                drug_manufacturer=drug_manufacturer_obj,
                gst=gst,
                uom_code=measuring_unit_obj.name,
                mcm_name=commodity_category_obj.name,
            )

            # distribution_center = DistributionCenter.objects.get(id=dc_id)

            # DcCommodity.objects.create(
            #     distribution_center=distribution_center,
            #     commodity=commodity,
            #     min_available_qty=min_available_qty,
            #     max_available_qty=max_available_qty,
            #     max_qty_allowed_per_order=max_qty_allowed_per_order,
            #     minimum_order_quantity=minimum_order_quantity
            # )

            # commodities = Commodity.objects.all()
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
