import sys, traceback

from rest_framework import status as Status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from account.models import Retailer

from crm.models import UserType, RequestType, ServiceRequest, RetailerServiceRequest

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def create_service_request_retailer(request):
    output = {}
    data = request.data

    try:
        typ = 'retailer'
        retailer_id = data['retailerId']
        request_type = data['requestType']
        description = data['description']
        
        try:
            retailer = Retailer.objects.get(id=retailer_id)
            try:
                user_type = UserType.objects.get(user_type=typ)
                req_typ = RequestType.objects.get(request_type=request_type)
                service_request = ServiceRequest.objects.create(
                        user_type=user_type,
                        request_type=req_typ,
                        name=retailer.user.name,
                        email=retailer.user.email,
                        phone_no=retailer.user.phone,
                        description=description
                    )
                retailer_service_request = RetailerServiceRequest.objects.create(
                        service_request=service_request,
                        retailer=retailer
                )
                output['status'] = 'success'
                output['status_text'] = 'Successfully requested the service'
                status = Status.HTTP_200_OK
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Failed to request the service'
                status = Status.HTTP_400_BAD_REQUEST
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'Invalid Retailer'
            status = Status.HTTP_401_UNAUTHORIZED
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = "failed"
        output['status_text'] = f'key error: {str(e)}'
        status = Status.HTTP_400_BAD_REQUEST
    
    return Response(output, status=status)
