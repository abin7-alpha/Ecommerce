import sys, traceback

from rest_framework import status as Status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from order.models import ShippingVendor
from order.api.serializers.shipping_vendor import ShippingVendorSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_shipping_vendors(request):
    output = {}

    try:
        shipping_vendors = ShippingVendor.objects.filter(is_active=True).all()
        vendor_serializer = ShippingVendorSerializer(shipping_vendors, many=True)
        output['status'] = 'success'
        output['status_text'] = 'successfully fetched all the vendors'
        output['shipping_vendors'] = vendor_serializer.data
        status = Status.HTTP_200_OK
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'failed to fetch the vendors'
        status = Status.HTTP_404_NOT_FOUND

    return Response(output, status=status)