import json, sys, traceback

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from commodity.models import DcCommodityBatch
from office.models import DistributionCenter

@api_view(['POST',])
@permission_classes([IsAuthenticated])
def get_commodities_by_region(request):
    # data = json.loads(request.data)
    data = request.data
    output = {}

    try:
        user_name = data['user']
        dist_center_id = data['distCenterId']

        try:
            user = User.objects.get(username=user_name)
        except:
            output['status'] = ['failed']
            output['status_txt'] = ['The user with this credential is not valid']
            return Response(json.dumps(output), status=status.HTTP_404_NOT_FOUND)
        
        distribution_center = DistributionCenter.objects.get(id=dist_center_id)

        if dist_center_id == 1:
            output['status'] = 'success'
            output['status_txt'] = 'Commodities by region karnataka fetched successfully.'
            dist_commodity_bathches_karnataka = DcCommodityBatch.objects.filter(distribution_center=distribution_center)
            output['dist_com_batches_karnataka'] = dist_commodity_bathches_karnataka

        if dist_center_id == 2:
            output['status'] = 'success'
            output['status_txt'] = 'Commodities by region karnataka and kerala fetched successfully.'
            dist_commodity_bathches_karnataka = DcCommodityBatch.objects.filter(distribution_center=distribution_center)
            dist_commodity_bathches_kerala = DcCommodityBatch.objects.filter(distribution_center=2)
            output['dist_com_batches_karnataka'] = dist_commodity_bathches_karnataka
            output['dist_com_batches_kerala'] = dist_commodity_bathches_kerala

    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_txt'] = 'Failed to fetch commodities by region'
        return Response(json.dumps(output), status=status.HTTP_400_BAD_REQUEST)
    
    return Response(json.dumps(output), status=status.HTTP_200_OK)

@api_view(['GET',])
@permission_classes([IsAuthenticated])
def get_com(request):
    output = {"abin": "paul"}
    return Response(json.dumps(output), status=status.HTTP_200_OK)
