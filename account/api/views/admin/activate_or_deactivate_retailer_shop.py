import traceback, sys

from account.models import RetailerShop
from account.decorators import is_retailer_manager
from account.api.serializers.retailer_shop import RetailerShopSerializer

from rest_framework import status as Status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
@is_retailer_manager()
def activate_or_deactivate_shop(request):
    output = {}
    data = request.data

    try:
        shop_id = data['shopId']
        is_active = data['isActive']

        try:
            retailer_shop = RetailerShop.objects.get(id=shop_id)
            try:
                retailer_shop.is_active = is_active
                retailer_shop.save()

                retailer_shop_serializer = RetailerShopSerializer(retailer_shop)

                output['status'] = 'success'
                output['status_text'] = 'Successfully updated the retailer shop'
                output['retailer_shop'] = retailer_shop_serializer.data
                status = Status.HTTP_200_OK
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Failed to update the retailer shop'
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