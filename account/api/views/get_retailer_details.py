import traceback
import sys

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from account.models import Retailer, BasicUser
from account.api.serializers.retailer_serializer import RetailerSerializer

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def get_retailer_details(request):
    # data = json.loads(request.data)
    data = request.data

    try:
        email = data['userEmail']
        # name = data['userName']
        output = {}
        
        try:
            user = User.objects.get(email=email)
            basic_user = BasicUser.objects.get(django_user=user)
            try:
                retailer = Retailer.objects.get(user=basic_user)
                serializer = RetailerSerializer(retailer)
                output['status'] = 'success'
                output['status_txt'] = 'Successfully fetched the details of Retailer'
                output['retailer_data'] = serializer.data
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_txt'] = 'No Retailer has been found'
                return Response(output, status=status.HTTP_404_NOT_FOUND)
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_txt'] = 'No user has been found with this credentials'
            return Response(output, status=status.HTTP_404_NOT_FOUND)
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_txt'] = 'Check the validity of credentials ad try again'
        return Response(output, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(output, status=status.HTTP_200_OK)
