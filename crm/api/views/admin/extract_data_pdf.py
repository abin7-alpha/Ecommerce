import traceback
import sys

from rest_framework import status as Status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from crm.extract_data import get_extracted_data

@api_view(['POST',])
@permission_classes([IsAuthenticated, ])
def extract_data_from_pdf(request):
    output={}
    if request.method == 'POST':
        try:
            file = request.FILES['file']
            try:
                user_data, vendordata = get_extracted_data(file)
                output['status']="success"
                output['vendor_data'] = vendordata
                output['user_data'] = user_data
                status = Status.HTTP_200_OK
            except:
                traceback.print_exc(file=sys.stdout)
                output['status']="failed"
                output['status_text']="Error While exracting the data"
                status = Status.HTTP_400_BAD_REQUEST
        except KeyError as e:
            output['status']="failed"
            output['status_text']= f"Key Error: {e}"
            traceback.print_exc(file=sys.stdout)
            status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)
