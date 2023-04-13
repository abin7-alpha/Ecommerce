import sys, traceback
import asyncio
import time

from rest_framework import status as Status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from commodity.models import DcCommodityBatch, DcCommodityBatchLog, DcCommodity
from commodity.api.serializers.dc_commodity_batch import DcCommodityBatchSerializer
from commodity.api.serializers.dc_commodity import DcCommodityForBatchSerializer

from account.functions import stock_available_send_notification
from account.decorators import is_logistics_manager

from asgiref.sync import async_to_sync, sync_to_async

@api_view(['POST',])
@permission_classes([IsAuthenticated, ])
@is_logistics_manager()
def update_commodity_batch_available_quantity(request):
    """To add or update the batch available quantity of the dcCommodity"""
    data = request.data
    output = {}

    try:
        batch_id = int(data['commodityBatchId'])
        batch_available_quantity = float(data['batchAvailableQuantity'])
        qty_change_type = data['quantityChangeType']
        try:
            commodity_batch = DcCommodityBatch.objects.get(id=batch_id)
            try:
                #Check if the batch quantity is a multiple of minimum order quantity
                
                if batch_available_quantity % commodity_batch.minimum_order_quantity != 0:
                    output['status'] = 'failed'
                    output['status_text'] = 'Batch quantity must be a multiple of minimum order quantity'
                    status = Status.HTTP_400_BAD_REQUEST
                    return Response(output, status=status)

                #Check if the quantity greater than current quantity
                if commodity_batch.available_quantity >= batch_available_quantity:
                    output['status'] = 'failed'
                    output['status_text'] = 'Updating batch quantity must be greater than current batch available quantity'
                    status = Status.HTTP_400_BAD_REQUEST
                else:    
                    dc_commodity = commodity_batch.dc_commodity
                    dc_commodity.available_quantity -= commodity_batch.available_quantity
                    dc_commodity.save()
                    commodity_batch.available_quantity = batch_available_quantity
                    commodity_batch.save()
                    dc_commodity.available_quantity += commodity_batch.available_quantity
                    dc_commodity.save()

                    DcCommodityBatchLog.objects.create(
                        batch=commodity_batch,
                        qty_change=batch_available_quantity,
                        change_type=qty_change_type,
                        available_quantity=commodity_batch.available_quantity
                    )

                    batch_serializer = DcCommodityBatchSerializer(commodity_batch)
                    # commodities = DcCommodity.objects.all()
                    # commodity_serializer = DcCommodityForBatchSerializer(commodities, many=True)
                    # start_time = time.time()

                    stock_available_send_notification(dc_commodity)

                    output['status'] = 'success'
                    output['status_text'] = 'succesfully updated the Commodity Batch available quantity'
                    output['updated_batch'] = batch_serializer.data
                    # output['dcCommodities'] = commodity_serializer.data
                    status = Status.HTTP_200_OK
                    return Response(output, status=status)
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Failed to update the Commodity Batch available quantity'
                status = Status.HTTP_400_BAD_REQUEST
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'Failed to fetch commodity batch'
            status = Status.HTTP_400_BAD_REQUEST
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = f'Key Error: {e}'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)