import traceback
import sys
import string
import random

from rest_framework import status as Status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from account.models import Retailer
from account.functions import get_amount_out_standing, get_last_sales, get_monthly_till_date
from account.functions import get_recent_order, get_yearly_till_date, out_standing_above_thirty_days

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def get_dashboard_data(request):
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
            output['annual_year_till_date'] = get_yearly_till_date(retailer_obj)
            output['monthly_till_date'] = get_monthly_till_date(retailer_obj)
            output['amount_outstanding'] = get_amount_out_standing(retailer_obj)
            output['total_no_orders'] = get_last_sales(retailer_obj)
            output['recent_order'] = get_recent_order(retailer_obj)
            output['outstanding_above_thirty_days'] = out_standing_above_thirty_days(retailer_obj)
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
