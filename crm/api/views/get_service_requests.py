import sys, traceback

from pytz import timezone
from datetime import timedelta, datetime

from rest_framework import status as Status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from crm.models import RetailerServiceRequest
from crm.api.serializers.retailer_service_request import RetailerServiceRequestSerializer

from account.models import Retailer

@api_view(['POST',])
@permission_classes([IsAuthenticated, ])
def get_service_requests_retailer(request):
    output = {}
    data = request.data

    try:
        retailer_id = data['retailerId']

        try:
            months = None
            if data['noMonths']:
                months = data['noMonths']
            else:
                raise Exception
        except:
            months = None

        try:
            retailer = Retailer.objects.get(id=retailer_id)
            try:
                if not months:
                    retailer_service_requests = RetailerServiceRequest.objects.filter(retailer=retailer).order_by('-created')
                    retailer_request_serializer = RetailerServiceRequestSerializer(retailer_service_requests, many=True)
                    output['status'] = 'success'
                    output['status_text'] = 'successfully fetched all the requests'
                    if not retailer_request_serializer.data:
                        raise Exception
                    output['requests'] = retailer_request_serializer.data
                    status = Status.HTTP_200_OK
                else:
                    no_days = months * 30
                    current_date = timezone('Asia/Kolkata').localize(datetime.now()) + timedelta(1)
                    formated_current_date = current_date.strftime("%Y-%m-%d")
                    start_date = current_date - timedelta(no_days)
                    formated_start_date = start_date.strftime("%Y-%m-%d")
                    retailer_service_requests = RetailerServiceRequest.objects.filter(retailer=retailer).filter(created__range=(formated_start_date, formated_current_date)).order_by('-created')
                    retailer_request_serializer = RetailerServiceRequestSerializer(retailer_service_requests, many=True)
                    output['status'] = 'success'
                    output['status_text'] = 'successfully fetched all the requests'
                    if not retailer_request_serializer.data:
                        raise Exception
                    output['requests'] = retailer_request_serializer.data
                    status = Status.HTTP_200_OK
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Failed to fetched all the requests'
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
                