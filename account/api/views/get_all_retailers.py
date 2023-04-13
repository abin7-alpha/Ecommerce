import sys, traceback

from rest_framework import status as Status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.models import Retailer
from account.api.serializers.retailer_serializer import RetailerSerializer
from account.decorators import is_retailer_manager

from office.models import DistributionCenter

from django.core.exceptions import ObjectDoesNotExist

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@is_retailer_manager()
def get_all_retailers(request):
    output = {}

    try:
        try:
            dc_id = int(request.query_params.get('dcId'))
            dc = DistributionCenter.objects.get(id=dc_id)
            retailers = Retailer.objects.all().filter(dc=dc)
        except:
            retailers = Retailer.objects.all()
        retailer_serializer = RetailerSerializer(retailers, many=True)
        output['status'] = 'success'
        output['status_text'] = 'successfully fetched all the Retailers'
        output['retailers'] = retailer_serializer.data
        status = Status.HTTP_200_OK
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'failed to fetch the Retailers'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@is_retailer_manager()
def search_all_retailer(request):
    output = {}
    data = request.data
    print(data)

    try:
        try:
            search_key = data['searchKey']
            try:
                print("hi.")
                retailer_id = int(search_key)
                print(retailer_id)
                try:
                    dc_id = data['dcId']
                    dc = DistributionCenter.objects.get(id=dc_id)
                    retailer = Retailer.objects.get(id=retailer_id, dc=dc)
                except:
                    retailer = Retailer.objects.get(id=retailer_id)

                retailer_serializer = RetailerSerializer(retailer)

                output['status'] = 'success'
                output['status_text'] = 'successfully fetched all the Retailers'
                output['retailers'] = [retailer_serializer.data]
                status = Status.HTTP_200_OK
            except:
                try:
                    dc_id = data['dcId']
                    dc = DistributionCenter.objects.get(id=dc_id)
                    retailers = Retailer.objects.filter(user__name__icontains=search_key, dc=dc)
                except:
                    retailers = Retailer.objects.filter(user__name__icontains=search_key)
                retailer_serializer = RetailerSerializer(retailers, many=True)

                output['status'] = 'success'
                output['status_text'] = 'successfully fetched all the Retailers'
                output['retailers'] = retailer_serializer.data
                status = Status.HTTP_200_OK
        except:
            try:
                dc_id = data['dcId']
                dc = DistributionCenter.objects.get(id=dc_id)
                retailers = Retailer.objects.all().filter(dc=dc)
            except:
                retailers = Retailer.objects.all()
            retailer_serializer = RetailerSerializer(retailers, many=True)
            output['status'] = 'success'
            output['status_text'] = 'successfully fetched all the Retailers'
            output['retailers'] = retailer_serializer.data
            status = Status.HTTP_200_OK
        # except:
        #     traceback.print_exc(file=sys.stdout)
        #     output['status'] = 'failed'
        #     output['status_text'] = 'failed to fetch the Retailers'
        #     status = Status.HTTP_400_BAD_REQUEST
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = f'{e}: Key Error'
        status = Status.HTTP_400_BAD_REQUEST
    
    return Response(output, status=status)
    
            

