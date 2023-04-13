import traceback
import sys
from datetime import datetime

from rest_framework import status as Status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser 

from order.convert_pdf import get_pdf_data
from order.models import RetailerPayment
from order.functions import convert_string_to_number

from account.models import Retailer

@api_view(['POST',])
@parser_classes([FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def import_data_from_pdf(request):
    try:
        output = {}
        file = request.FILES['file']
        data = request.data

        pdf_data = get_pdf_data(file)
        retailer_id = data['retailerId']
        try:
            retailer = Retailer.objects.get(id=retailer_id)
            try:
                for data in pdf_data:
                    if data['Vch Type'] == 'Sales':
                        continue
                    else:
                        # print(convert_string_to_number(data['Credit']))
                        retailer_payment = RetailerPayment.objects.create(
                            retailer=retailer, 
                            txn_id=data['Vch No.'],
                            amount=convert_string_to_number(data['Credit']),
                            product_info=data['Particulars']
                        )
                        retailer_payment.payment_mode = data['Particulars']
                        retailer_payment.is_online_payment = True
                        retailer_payment.is_verified_by_admin = True
                        retailer_payment.status = True
                        try:
                            retailer_payment.created = datetime.strptime(data['Date'], '%d-%b-%y')
                        except:
                            pass
                        retailer_payment.save()
                        output['status'] = 'success'
                        output['status_text'] = 'Successfully imported data from pdf'
                        status = Status.HTTP_200_OK
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Failed to import data from pdf'
                status = Status.HTTP_400_BAD_REQUEST
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'Invalid Retailer'
            status = Status.HTTP_400_BAD_REQUEST
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = f'{e}: Key Error'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)            
