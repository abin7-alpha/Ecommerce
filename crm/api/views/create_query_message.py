import traceback
import sys
import asyncio

from rest_framework import status as Status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from crm.models import ServiceRequest,QueryLog, RetailerServiceRequest
from crm.api.serializers.sevice_requests import ServiceRequestSerializer
from crm.functions import send_reply

from account.models import RetailerNotification, NotificationType

@api_view(['POST',])
@permission_classes([IsAuthenticated, ])
def create_message_query(request):
    data = request.data
    output = {}

    try:
        # query_id = data['queryId']
        retailer_service_request_id = data['retailerServiceRequestId']
        message = data['message']
        # is_retailer_query = data['isRetailerQuery']
        try:
            try:
                # query = None
                # if is_retailer_query:
                # retailer_service_request_id = data['retailerServiceRequestId']
                retailer_query = RetailerServiceRequest.objects.get(id=retailer_service_request_id)
                retailer = retailer_query.retailer
                query = retailer_query.service_request
                notification_type = NotificationType.objects.get(name='Service')
                RetailerNotification.objects.create(
                    retailer=retailer,
                    title='Service Request Replied',
                    notification_type=notification_type,
                    content=message,
                )
                # else:
                #     query = ServiceRequest.objects.get(id=query_id)

                msg_obj = QueryLog.objects.create(
                    log=message,
                    is_admin=False
                )

                query.query_log.add(msg_obj)
                query.save()

                output['status'] = 'success'
                output['status_text'] = 'successfully messaged to the admin'
                output['orders'] = ServiceRequestSerializer(query).data
                status = Status.HTTP_200_OK
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Failed to message the admin'
                status = Status.HTTP_400_BAD_REQUEST
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'Invalid query details'
            status = Status.HTTP_400_BAD_REQUEST
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = f'Key Error: {e}'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)