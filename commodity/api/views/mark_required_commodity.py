import traceback
import sys
import json

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from commodity.models import DistributionStoreIndent

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def mark_commodity_not_required(request):
    # data = json.loads(request.data)
    data = request.data

    try:
        dist_store_indent_id = data['distStoreId']

        output = {}
        
        try:
            dist_store_indent = DistributionStoreIndent.objects.filter(is_active=True).filter(id=dist_store_indent_id)
            try:
                dist_store_indent.update(is_deleted=True)
                dist_store_indent.update(is_active=False)
                output['status'] = 'success'
                output['status_txt'] = 'Successfully marked the commodity not required anymore'
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_txt'] = 'Failed to mark the commodity as not required anymore'
                return Response(output, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_txt'] = 'No distribution store indent has been found'
            return Response(output, status=status.HTTP_404_NOT_FOUND)
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_txt'] = 'Check the validity of credentials ad try again'
        return Response(output, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(output, status=status.HTTP_200_OK)
