import sys, traceback
import json

from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from account.functions import send_sms, add_amount_out_standing

@api_view(['POST',])
@permission_classes([AllowAny,])
def send_SMS(request):
    output = {}
    # data = json.loads(request.data)
    data = request.data
    message = data['message']
    number = data['number']

    try:
        add_amount_out_standing()
        value = send_sms(message, number)
        print(value)
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(data, status=status.HTTP_200_OK)
