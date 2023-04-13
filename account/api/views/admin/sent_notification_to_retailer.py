import traceback, sys

from account.models import Retailer, RetailerNotification
from account.api.serializers.retailer_serializer import RetailerOrderSerializer, RetailerSerializer
from account.decorators import is_retailer_manager

from rest_framework import status as Status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
@is_retailer_manager()
def send_notification_to_retailer(request):
    output = {}
    data = request.data

    try:
        retailer_id = data['retailerId']
        message = data['message']
        header = data['header']
        is_in_kannada = data['isSendInKannada']

        try:
            retailer = Retailer.objects.get(id=retailer_id)
            try:
                RetailerNotification.objects.create(
                    retailer=retailer,
                    title=header,
                    content=message,
                    is_in_kannada=is_in_kannada
                )

                retailer_serializer = RetailerOrderSerializer(retailer)

                retailers = Retailer.objects.all()
                retailers_serializer = RetailerSerializer(retailers, many=True)

                output['status'] = 'success'
                output['status_text'] = 'Successfully Notified the Retailer'
                output['retailer'] = retailer_serializer.data
                output['retailers'] = retailers_serializer.data
                status = Status.HTTP_200_OK
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Failed to Notify the retailer'
                status = Status.HTTP_400_BAD_REQUEST
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'Retailer not found'
            status = Status.HTTP_400_BAD_REQUEST
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = f'Invalid data: Key error: {e}'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)
                

