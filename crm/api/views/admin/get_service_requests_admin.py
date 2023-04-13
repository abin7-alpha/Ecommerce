import sys, traceback

from rest_framework import status as Status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from crm.models import ServiceRequest, RetailerServiceRequest
from crm.api.serializers.sevice_requests import ServiceRequestSerializer
from crm.api.serializers.retailer_service_request import RetailerServiceRequestSerializer

from account.decorators import is_retailer_manager

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@is_retailer_manager()
def get_all_service_requests_admin(request):
    output = {}

    try:
        service_requests = ServiceRequest.objects.all().order_by('-created')
        service_request_serializer = ServiceRequestSerializer(service_requests, many=True)

        retailer_service_requests = RetailerServiceRequest.objects.all().order_by('-created')
        retailer_service_requests_serializer = RetailerServiceRequestSerializer(retailer_service_requests, many=True)

        output['status'] = 'success'
        output['status_text'] = 'successfully fetched all the requests'
        output['service_requests'] = service_request_serializer.data
        output['retailer_service_requests'] = retailer_service_requests_serializer.data
        status = Status.HTTP_200_OK
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'failed to fetch the requests'
        status = Status.HTTP_404_NOT_FOUND

    return Response(output, status=status)