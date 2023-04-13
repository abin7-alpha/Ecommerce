import sys, traceback
import asyncio

from rest_framework import status as Status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from commodity.models import DcCommodity, DcCommodityBatch
from commodity.api.serializers.dc_commodity_batch import DcCommodityBatchSerializer
from commodity.api.serializers.dc_commodity import DcCommodityForBatchSerializer

from account.functions import stock_available_send_notification
from account.decorators import is_logistics_manager


@api_view(['POST',])
@permission_classes([IsAuthenticated, ])
@is_logistics_manager()
def add_commodity_batch(request):
    data = request.data
    output = {}

    try:
        dc_commodity_id = data['dcCommodityId']
        batch_price = data['batchPrice']
        batch_id = data['batchId']
        batch_available_quantity = float(data['batchAvailableQuantity'])
        batch_minimum_order_quantity = data['minimumOrderQuantity']
        batch_expiry_date = data['expiryDate']

        try:
            dc_commodity = DcCommodity.objects.get(id=dc_commodity_id)
            dc_commodity_batch = DcCommodityBatch.objects.create(
                    dc_commodity=dc_commodity,
                    batch_id=batch_id,
                    price=batch_price,
                    available_quantity=batch_available_quantity,
                    minimum_order_quantity=batch_minimum_order_quantity,
                    expiry_date=batch_expiry_date.split("T")[0]
            )
            if dc_commodity.available_quantity:
                dc_commodity.available_quantity += batch_available_quantity
                dc_commodity.save()
            else:
                dc_commodity.available_quantity = batch_available_quantity + 0
                dc_commodity.save()

            stock_available_send_notification(dc_commodity)
            
            batch_serializer = DcCommodityBatchSerializer(dc_commodity_batch)

            commodities = DcCommodity.objects.all()
            commodity_serializer = DcCommodityForBatchSerializer(commodities, many=True)

            output['status'] = 'success'
            output['status_text'] = 'succesfully updated the Commodity Batch'
            output['added_batch'] = batch_serializer.data
            output['dcCommodities'] = commodity_serializer.data
            status = Status.HTTP_200_OK
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'failed to update the Commodity Batch'
            status = Status.HTTP_400_BAD_REQUEST
    
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = f'Key Error: {e}'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)




        

