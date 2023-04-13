import sys, traceback

from rest_framework import status as Status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view

from commodity.models import CommodityCategory, CommodityGroup, DrugManufacturer, CommodityMeasuringUnits
from commodity.api.serializers.commodity_category import CommodityCategorySerializer
from commodity.api.serializers.commodity_group import CommodityGroupSerializer
from commodity.api.serializers.drug_manufacturer import DrugManufacturerSerializer
from commodity.api.serializers.measuring_unit import CommodityMeasuringUnitsSerializer

@api_view(['GET',])
@permission_classes([IsAuthenticated,])
def get_commodity_group_and_category(request):
    output = {}

    try:
        categories = CommodityCategory.objects.filter(is_active=True)
        categories_serializer = CommodityCategorySerializer(categories, many=True)

        groups = CommodityGroup.objects.filter(is_active=True)
        groups_serializer = CommodityGroupSerializer(groups, many=True)

        drug_manufactures = DrugManufacturer.objects.filter(is_active=True)
        manufacturer_serializer = DrugManufacturerSerializer(drug_manufactures, many=True)

        measuring_units = CommodityMeasuringUnits.objects.filter(is_active=True)
        measuring_unit_serializer = CommodityMeasuringUnitsSerializer(measuring_units, many=True)

        output['status'] = 'success'
        output['status_text'] = 'Successfully fetched Commodity groups and categories'
        output['categories'] = categories_serializer.data
        output['groups'] = groups_serializer.data
        output['manufacturers'] = manufacturer_serializer.data
        output['measuring_units'] = measuring_unit_serializer.data
        status = Status.HTTP_200_OK
    
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'Failed to fetch Commodity groups and categories'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status)
