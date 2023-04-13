import traceback
import sys

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from account.models import Retailer, BasicUser, RetailerNotification
from account.api.serializers.retailer_notification import RetailerNotificationSerializer

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def get_retailer_notifications(request):
    data = request.data
    # data = json.loads(request.data)

    try:
        retailer_id = data['retailerId']
        # name = data['userName']
        output = {}
        
        try:
            retailer = Retailer.objects.get(id=retailer_id)
            # print(retailer)
            try:
                retailer_notificaitons = RetailerNotification.objects.filter(retailer=retailer).order_by('-created')
                serializer = RetailerNotificationSerializer(retailer_notificaitons, many=True)
                output['status'] = 'success'
                output['status_txt'] = 'Successfully fetched the Retailer Notifications'
                output['retailer_data'] = serializer.data
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_txt'] = 'No Retailer Notifications has been found'
                return Response(output, status=status.HTTP_404_NOT_FOUND)
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_txt'] = 'No user has been found with this credentials'
            return Response(output, status=status.HTTP_404_NOT_FOUND)
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_txt'] = 'Check the validity of credentials ad try again'
        return Response(output, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(output, status=status.HTTP_200_OK)
