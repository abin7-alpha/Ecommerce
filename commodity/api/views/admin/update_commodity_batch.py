import sys, traceback

from pytz import timezone
from datetime import datetime

from rest_framework import status as Status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from commodity.models import DcCommodityBatch
from commodity.api.serializers.dc_commodity_batch import DcCommodityBatchSerializer

from account.decorators import is_logistics_manager


@api_view(['POST',])
@permission_classes([IsAuthenticated, ])
@is_logistics_manager()
def update_commodity_batch(request):
    data = request.data
    output = {}
    current_date = timezone('Asia/Kolkata').localize(datetime.now())

    try:
        batch_id = int(data['commodityBatchId'])
        # batch_price = float(data['batchPrice'])
        # batch_available_quantity = float(data['batchAvailableQuantity'])
        batch_minimum_order_quantity = float(data['minimumOrderQuantity'])
        batch_expiry_date = data['expiryDate']
        print(batch_expiry_date)

        try:
            batch_obj = DcCommodityBatch.objects.get(id=batch_id)
            dc_commodity = batch_obj.dc_commodity
            # dc_commodity.available_quantity -= batch_obj.available_quantity
            # dc_commodity.save()
            # batch_obj.price = batch_price
            # batch_obj.available_quantity = batch_available_quantity
            batch_obj.expiry_date = batch_expiry_date.split("T")[0]
            batch_obj.minimum_order_quantity = batch_minimum_order_quantity
            batch_obj.updated = current_date
            batch_obj.save()
            # dc_commodity.available_quantity += batch_obj.available_quantity
            # dc_commodity.save()

            batch_serializer = DcCommodityBatchSerializer(batch_obj)

            output['status'] = 'success'
            output['status_text'] = 'succesfully updated the Commodity Batch'
            output['updated_batch'] = batch_serializer.data
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

