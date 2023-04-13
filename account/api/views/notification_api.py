import sys, traceback

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from account.functions import stock_available_send_notification

@api_view(['GET'])
@permission_classes([AllowAny,])
def notify_user(request):
    output = {}
    try:
        stock_available_send_notification()
        output['status'] = 'sucess'
        output['status_text'] = 'succesfully sent all the notificatios for retailer'
        return Response(output, status=status.HTTP_200_OK)
    except:
        output['status'] = 'failed'
        output['status_text'] = 'failed to sent all the notificatios for retailer'
        return Response(output, status=status.HTTP_400_BAD_REQUEST)
