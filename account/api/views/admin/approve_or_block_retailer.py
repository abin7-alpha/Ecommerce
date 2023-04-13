import json
import traceback, sys

from account.models import Retailer, BasicUser
from account.api.serializers.retailer_serializer import RetailerOrderSerializer, RetailerSerializer
from account.decorators import is_retailer_manager

from rest_framework import status as Status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
@is_retailer_manager()
def approve_or_block_retailer(request):
    data = request.data
    output = {}
    
    try:
        retailer_id = data['retailerId']
        is_active = data['isActive']
        is_admin_verified = data['isAdminVerified']
        try:
            retailer = Retailer.objects.get(id=retailer_id)
            user_id = retailer.user.id
            try:
                Retailer.objects.filter(id=retailer_id).update(is_admin_verified=is_admin_verified)
                BasicUser.objects.filter(id=user_id).update(is_active=is_active)
                retailer_serializer = RetailerOrderSerializer(retailer)

                retailers = Retailer.objects.all()
                retailers_serializer = RetailerSerializer(retailers, many=True)

                output['status'] = 'success'
                output['status_text'] = 'Successfully modified the Retailer'
                output['retailer'] = retailer_serializer.data
                output['retailers'] = retailers_serializer.data
                status = Status.HTTP_200_OK
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Failed to modify the retailer configurations'
                status = Status.HTTP_400_BAD_REQUEST
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'Retailer not found'
            status = Status.HTTP_400_BAD_REQUEST
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = f'Invalid data: Key error: {e}'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)
