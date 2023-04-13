import sys, traceback
from pytz import timezone
from datetime import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from account.models import Retailer

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def record_notification_view_date(request):
    output = {}
    data = request.data

    current_date_time = timezone('Asia/Kolkata').localize(datetime.now())
    print(current_date_time)

    try:
        retailer_id = data['retailerId']
        try:
            retailer = Retailer.objects.get(id=retailer_id)
            try:
                retailer.last_notification_view = current_date_time
                retailer.save()
                
                output['status'] = 'success'
                output['status_txt'] = 'Successfully recorded notified date'
                return Response(output, status=status.HTTP_200_OK)
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_txt'] = 'Failed to record the notified date'
                return Response(output, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_txt'] = 'Invalid retailer'
            return Response(output, status=status.HTTP_400_BAD_REQUEST)
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_txt'] = f'{e}: Key Error'
        return Response(output, status=status.HTTP_400_BAD_REQUEST)
    