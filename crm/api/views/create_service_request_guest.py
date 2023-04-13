import sys, traceback

from rest_framework import status as Status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from crm.models import UserType, RequestType, ServiceRequest

@api_view(['POST',])
@permission_classes([AllowAny,])
def create_service_request_guest(request):
    output = {}
    data = request.data

    try:
        typ = 'guest'
        request_type = data['requestType']
        description = data['description']
        name = data['userName']
        email = data['userEmail']
        phone = data['userPhone']
        
        try:
            user_type = UserType.objects.get(user_type=typ)
            req_typ = RequestType.objects.get(request_type=request_type)
            service_request = ServiceRequest.objects.create(
                    user_type=user_type,
                    request_type=req_typ,
                    name=name,
                    email=email,
                    phone_no=phone,
                    description=description
                )
            output['status'] = 'success'
            output['status_text'] = 'Successfully requested the service'
            status = Status.HTTP_200_OK
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'Failed to request the service'
            status = Status.HTTP_400_BAD_REQUEST
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = "failed"
        output['status_text'] = f'key error: {str(e)}'
        status = Status.HTTP_400_BAD_REQUEST
    
    return Response(output, status=status)