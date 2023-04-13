import traceback, sys

from account.models import Retailer, RetailerShop, Addresses, AddressType
from account.api.serializers.retailer_shop import RetailerShopSerializer
from account.decorators import is_retailer_manager

from rest_framework import status as Status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
@is_retailer_manager()
def create_new_retailer_shop(request):
    output = {}
    data = request.data

    try:
        retailer_id = data['retailerId']
        shop_code = data['shopCode']
        shop_name = data['shopName']
        shop_phone = data['shopPhone']
        country = data['country']
        state = data['state']
        city = data['city']
        zip_code = data['zipCode']
        line1 = data['line1']

        try:
            line2 = data['line2']
        except:
            line2 = ""

        try:
            line3 = data['line3']
        except:
            line3 = ""

        try:
            shop_pic_in = data['shopPicIn']
        except:
            shop_pic_in = ""
        try:
            shop_pic_out = data['shopPicOut']
        except:
            shop_pic_out = ""

        try:
            retailer = Retailer.objects.get(id=retailer_id)
            try:
                address_type = AddressType.objects.get(name='Shop')

                shop_address = Addresses.objects.create(
                    line1=line1,
                    line2=line2,
                    line3=line3,
                    country=country,
                    state=state,
                    city=city,
                    zipcode=zip_code,
                    address_type=address_type
                )

                retailer_shop = RetailerShop.objects.create(
                    shop_address=shop_address,
                    shop_code=shop_code,
                    shop_name=shop_name,
                    shop_phone=shop_phone,
                    shop_pic_in=shop_pic_in,
                    shop_pic_out=shop_pic_out
                )

                retailer.shops.add(retailer_shop)

                retailer_shop_serializer = RetailerShopSerializer(retailer_shop)

                output['status'] = 'success'
                output['status_text'] = 'Successfully created new retailer store'
                output['retailer_shop'] = retailer_shop_serializer.data
                status = Status.HTTP_200_OK
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Failed to create the retailer store'
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