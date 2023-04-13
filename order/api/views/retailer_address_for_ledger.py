import traceback
import sys

from rest_framework import status as Status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from account.models import Retailer
from account.functions import get_yearly_till_date

from order.functions import get_total_credit

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def get_ledger_data(request):
    output = {}
    data = request.data
    try:
        retailer_id = data['retailerId']

        try:
            retailer_obj = Retailer.objects.get(id=retailer_id)
        except:
            status = Status.HTTP_404_NOT_FOUND
            output['status'] = 'failed'
            output['status_text'] = 'No retailer has been found'
        try:
            output['status'] = 'success'
            output['status_txt'] = 'Successfully fetched the dashboard data'
            output['total_debit'] = round(get_yearly_till_date(retailer_obj), 2) 
            output['total_credit'] = round(get_total_credit(retailer_obj), 2)
            output['closing_balance'] = round(output['total_debit'] + output['total_credit'], 2)
            status = Status.HTTP_200_OK
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_txt'] = 'Some of data were not found, we apologize for the inconvenience'
            status = Status.HTTP_404_NOT_FOUND
            return Response(output, status=status)
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_txt'] = 'Failed to fetch the dashboard data'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)