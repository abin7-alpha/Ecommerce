import openpyxl
import traceback
import sys
import random
import string

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser

from commodity.models import Commodity, CommodityMeasuringUnits, CommodityCategory, CommodityGroup
from commodity.models import DcCommodity, DcCommodityBatch
from commodity.models import DrugManufacturer
from commodity.functions import get_moq

from commodity.convert_xlsx import xlsx_data

from office.models import DistributionCenter

def get_data(file):
    wb = openpyxl.load_workbook(file)
    sheet = wb.active

    data = xlsx_data(sheet)

    return data

@api_view(['POST',])
@parser_classes([FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def add_data_com(request):
    try:
        output = {}
        status_failed = 'failed'
        status_success = 'success'
        file = request.FILES['file']
        data = request.data

        xlsx_data = get_data(file)
        dc_id = data['dcId']
        distribution_center = DistributionCenter.objects.get(id=dc_id)
        try:

            for instance in xlsx_data['data']:
                measuring_unit, created = CommodityMeasuringUnits.objects.get_or_create(name=instance['UOM '])
                commodity_category, created = CommodityCategory.objects.get_or_create(name=instance['Drug Category'])
                commodity_group, created = CommodityGroup.objects.get_or_create(name=instance['Drug Group'])
                drug_manufacturer, created = DrugManufacturer.objects.get_or_create(name='syndicate')
                name = instance['Drug Name']
                # salt_name = instance['mm_saltname']
                mm_code = instance['Drug Code']
                # searchkey = instance['mm_searchkey']
                mcm_name = instance['Drug Category']
                uom_code = instance['UOM ']
                hsn_code = instance['Hsn Code']
                # is_active = False
                # if instance['Mm_IsActive'] == 'Yes':
                #     is_active = True
                mtm_name = instance['Drug Type']
                mrp = instance['MRP']
                
                try:
                    commodity = Commodity.objects.get(mm_code=mm_code)
                except:
                    commodity = Commodity.objects.create(measuring_unit=measuring_unit, commodity_category=commodity_category,
                                                        commodity_group=commodity_group, drug_manufacturer=drug_manufacturer,
                                                        name=name, mm_code=mm_code, gst=12, igst=0,
                                                        mcm_name=mcm_name, uom_code=uom_code, hsncode=hsn_code, 
                                                        mtm_name=mtm_name)
                    commodity.save()
                
                try:
                    dc_commodity = DcCommodity.objects.filter(distribution_center=distribution_center).get(commodity=commodity)
                    dc_commodity.available_quantity += instance['Qty']
                    dc_commodity.save()
                except:
                    dc_commodity = DcCommodity.objects.create(
                            distribution_center=distribution_center,
                            commodity=commodity,
                            available_quantity=instance['Qty'],
                            min_available_qty=float(100),
                            max_available_qty=float(1000),
                            max_qty_allowed_per_order=float(100),
                            minimum_order_quantity=float(10))
                # array_numbers = total_array_sum_tousand
                # print(array_numbers)
                # list_prices = [500, 300, 400, 450, 600, 650]
                # for instance in range(4):
                #     rand_idx = random.randrange(len(array_numbers))
                #     random_num = array_numbers[rand_idx]
                #     rand_idx2 = random.randrange(len(list_prices))
                #     random_num2 = list_prices[rand_idx2]
                try:
                    dc_commodity_batch = DcCommodityBatch.objects.filter(dc_commodity=dc_commodity).get(batch_id=instance['Batch No'])
                    dc_commodity_batch.available_quantity += instance['Qty']
                    dc_commodity_batch.save()
                except:
                    dc_commodity_batch = DcCommodityBatch.objects.create(
                        dc_commodity=dc_commodity,
                        batch_id=instance['Batch No'],
                        price=float(instance['Rate']),
                        mrp=mrp,
                        minimum_order_quantity=get_moq(int(instance['Qty'])),
                        available_quantity=float(instance['Qty']),
                        expiry_date=instance['Expiry Date']
                    )
                #     array_numbers.remove(random_num)
                # total_array_sum_tousand = [150, 350, 200, 300]
            
            # size = 5
            # for batch in DcCommodityBatch.objects.all():
            #     random_id = ''.join(random.choices(string.ascii_uppercase +
            #                     string.digits, k=size))
            #     batch.batch_id = random_id
            #     batch.save()
                    

            output['status'] = status_success
            output['status_text'] = 'Imported data and pushed to data base successfully'
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = status_failed
            output['status_text'] = 'failed to pushed to database'
            return Response(output, status=status.HTTP_400_BAD_REQUEST)
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = status_failed
        output['status_text'] = 'failed to import data from xlsx'
        return Response(output, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(output, status=status.HTTP_200_OK)
