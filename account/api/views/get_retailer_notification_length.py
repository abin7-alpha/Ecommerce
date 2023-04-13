import traceback
import sys

from pytz import timezone
from datetime import datetime

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from account.models import Retailer, RetailerNotification
from account.api.serializers.retailer_notification import RetailerNotificationSerializer

from django.utils.timezone import localtime

from pprint import pprint

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def get_retailer_notification_count(request):
    data = request.data
    current_date_time = timezone('Asia/Kolkata').localize(datetime.now())

    try:
        retailer_id = data['retailerId']
        output = {}        
        try:
            retailer = Retailer.objects.get(id=retailer_id)
            end_date = current_date_time
            start_date = retailer.last_notification_view
            # date_range = (datetime.combine(start_date, datetime.min.time()), datetime.combine(end_date, datetime.max.time()))
            try:
                retailer_notificaitons = RetailerNotification.objects.filter(retailer=retailer).filter(created__lte=end_date).filter(created__gte=start_date)
                serializer = RetailerNotificationSerializer(retailer_notificaitons, many=True)
                output['status'] = 'success'
                output['status_txt'] = 'Successfully fetched the Retailer Notifications'
                output['retailer_notification_count'] = len(serializer.data)
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
