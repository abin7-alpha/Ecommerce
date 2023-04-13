import traceback, sys

from account.models import Retailer, RetailerRecentSearch
from account.api.serializers.retailer_recent_search import RetailerRecentSearchSerializer

from rest_framework import status as Status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def get_retailer_recent_searches(request):
    data = request.data
    output = {}
    
    try:
        retailer_id = data['retailerId']
        try:
            retailer = Retailer.objects.get(id=retailer_id)
            try:
                recent_searches = RetailerRecentSearch.objects.filter(retailer=retailer)

                recent_serializer = RetailerRecentSearchSerializer(recent_searches, many=True)

                output['status'] = 'success'
                output['status_text'] = 'Successfully fetched the retailer recent searches'
                output['recent_searches'] = recent_serializer.data
                status = Status.HTTP_200_OK
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Failed to fetch the retailer recent searches'
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