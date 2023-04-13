import sys, traceback

from rest_framework import status as Status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from commodity.models import Commodity, CommodityMeasuringUnits, CommodityCategory, CommodityGroup, DrugManufacturer
from commodity.api.serializers.commodity import CommoditySerializer

from account.decorators import is_logistics_manager

@api_view(['POST',])
@permission_classes([IsAuthenticated, ])
@is_logistics_manager()
def update_commodity(request):
    data = request.data
    output = {}

    try:
        name = data['name']
        salt_name = data['saltName']
        mm_code = data['mmCode']
        gst = data['gst']
        hsn_code = data['hsnCode']
        mtm_name = data['mtmName']
        commodity_id = data['commodityId']

        measuring_unit = None
        try:
            if type(data['measuringUnit']) is dict:
                measuring_unit = data['measuringUnit']["id"]
            else:
                raise Exception
        except:
             measuring_unit = data['measuringUnit']

        commodity_category = None
        try:
            if type(data['commodityCategory']) is dict:
                commodity_category = data['commodityCategory']["id"]
            else:
                raise Exception
        except:
            commodity_category = data['commodityCategory']

        commodity_group = None
        try:
            if type(data['commodityGroup']) is dict:
                commodity_group = data['commodityGroup']["id"]
            else:
                raise Exception
        except:
            commodity_group = data['commodityGroup']
        
        drug_manufacturer = None
        try:
            if type(data['drugManufacturer']) is dict:
                drug_manufacturer = data['drugManufacturer']["id"]
            else:
                raise Exception
        except:
            drug_manufacturer = data['drugManufacturer']

        try:
            measuring_unit_obj = CommodityMeasuringUnits.objects.get(id=measuring_unit)
            commodity_category_obj = CommodityCategory.objects.get(id=commodity_category)
            commodity_group_obj = CommodityGroup.objects.get(id=commodity_group)
            drug_manufacturer_obj = DrugManufacturer.objects.get(id=drug_manufacturer)

            commodity = Commodity.objects.get(id=commodity_id)
            commodity.name=name
            commodity.salt_name=salt_name
            commodity.mm_code=mm_code
            commodity.hsncode=hsn_code
            commodity.searchkey=salt_name
            commodity.mtm_name=mtm_name
            commodity.measuring_unit=measuring_unit_obj
            commodity.commodity_category=commodity_category_obj
            commodity.commodity_group=commodity_group_obj
            commodity.drug_manufacturer=drug_manufacturer_obj
            commodity.gst=gst
            commodity.uom_code=measuring_unit_obj.name
            commodity.mcm_name=commodity_category_obj.name
            commodity.save()

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