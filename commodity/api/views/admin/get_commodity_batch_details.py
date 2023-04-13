import sys, traceback

from rest_framework import status as Status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from commodity.models import DcCommodityBatch
from commodity.api.serializers.dc_commodity_batch import DcCommodityBatchSerializer

from account.decorators import is_logistics_manager


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@is_logistics_manager()
def get_batch_details(request):
    output = {}
    data = request.data

    try:
        batch_id = data['batchId']
        try:
            commodity_batch = DcCommodityBatch.objects.get(id=batch_id)
            commodity_serializer = DcCommodityBatchSerializer(commodity_batch)
            output['status'] = 'success'
            output['status_text'] = 'successfully fetched the batch details'
            output['commodity_batch'] = commodity_serializer.data
            status = Status.HTTP_200_OK
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'failed to fetch the batch details'
            status = Status.HTTP_400_BAD_REQUEST
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = f'Key Error: {e}'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)