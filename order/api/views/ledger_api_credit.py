import traceback
import sys

from datetime import datetime, timedelta

from django.db.models import Q
from django.core.paginator import Paginator

from rest_framework import status as Status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from order.models import RetailerPayment, Order, OrderPayment
from order.api.serializers.order import OrderSerializerForOrderPayment
from order.api.serializers.retailer_payment import RetailerPaymentSerializer

from account.models import Retailer

from pprint import pprint

@api_view(['POST',])
@permission_classes([IsAuthenticated])
def get_ledger_credit(request):
    data = request.data
    output = {}

    try:
        retailer_id = data['retailerId']
        page_number = data['pageNumber']
        start_date_param = data['startDate']
        end_date_param = data['endDate']
        start_date_split = datetime.strptime(start_date_param, "%m/%d/%Y")
        end_date_split = end_date_param.split('/')
        start_date = start_date_split + timedelta(days=1)
        end_date = f'{end_date_split[2]}-{end_date_split[0]}-{end_date_split[1]}'
        
        try:
            retailer = Retailer.objects.get(id=retailer_id)
            retailer_credits = []
            try:
                retailer_payments = RetailerPayment.objects.filter(retailer=retailer).filter(created__range=(end_date, start_date)).order_by('-created')

                for payment in retailer_payments:
                    payment_serializer = RetailerPaymentSerializer(payment)
                    formated_payment = payment_serializer.data
                    try:
                        order_payment_with_retailer_payments = OrderPayment.objects.filter(retailer_payment=payment)
                        for order_payment in order_payment_with_retailer_payments:
                            if 'orders' not in formated_payment:
                                formated_payment['orders'] = [OrderSerializerForOrderPayment(order_payment.order).data]
                            else:
                                formated_payment['orders'].append(OrderSerializerForOrderPayment(order_payment.order).data)
                        retailer_credits.append(formated_payment)
                    except:
                        formated_payment['orders'] = None
                        retailer_credits.append(formated_payment)

                p = Paginator(retailer_credits, 9)
                current_page = p.page(page_number)

                output['status'] = 'success'
                output['status_text'] = 'Successfully Fetched all the retailer credits'
                output['total_pages'] = p.num_pages
                output['current_page_number'] = current_page.number
                output['previous'] = current_page.has_previous()
                output['next'] = current_page.has_next()
                output['count'] = p.count
                output['results'] = current_page.object_list

                status = Status.HTTP_200_OK
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Failed to fetch the retailer credits'
                status = Status.HTTP_400_BAD_REQUEST
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'Retailer not found'
            status = Status.HTTP_400_BAD_REQUEST
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = f'Invalid data: {e}'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)
