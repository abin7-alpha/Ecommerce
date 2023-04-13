import traceback
import sys
import asyncio

from rest_framework import status as Status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from order.models import Order
from order.api.serializers.order import OrderSerializer
from order.functions import get_order_data, sendOrderConfirmationMailToCustomer

@api_view(['POST',])
@permission_classes([IsAuthenticated, ])
def confirm_retailer_order_by_admin(request):
    data = request.data
    output = {}

    try:
        order_id = data['orderId']
        try:
            order = Order.objects.get(id=order_id)
            try:
                order.is_admin_verified = True
                order.save()

                total_other_charges, grand_total, total_normal_product_price = get_order_data(order)

                retailer = order.retailer
                
                if retailer.is_payment_check_required == True and not retailer.pending_amount_limit:
                    if not retailer.total_amount_outstanding:
                        retailer.total_amount_outstanding = order.amount + 0
                        retailer.save()
                    else:
                        retailer.total_amount_outstanding += order.amount
                        retailer.save()      

                elif retailer.is_payment_check_required == False:
                    if not retailer.total_amount_outstanding:
                        retailer.total_amount_outstanding = order.amount + 0
                        retailer.save()
                    else:
                        retailer.total_amount_outstanding += order.amount
                        retailer.save()

                elif retailer.is_payment_check_required:
                    if not retailer.total_amount_outstanding:
                        retailer.total_amount_outstanding = order.amount + 0
                        retailer.save()
                    else:
                        if retailer.total_amount_outstanding + order.amount > retailer.pending_amount_limit:
                            output['status'] = 'failed'
                            output['status_text'] = f'Retailer {retailer.pending_amount_limit} credit limit exceded, approval is not possible'
                            status = Status.HTTP_400_BAD_REQUEST
                            return Response(output, status=status)
                        else:
                            retailer.total_amount_outstanding += order.amount
                            retailer.save()
                
                asyncio.run(sendOrderConfirmationMailToCustomer(order, total_other_charges, total_normal_product_price))

                all_orders = Order.objects.all()
                all_orders_serializer = OrderSerializer(all_orders, many=True)

                output['status'] = 'success'
                output['status_text'] = 'successfully approved the order'
                output['orders'] = all_orders_serializer.data
                status = Status.HTTP_200_OK
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Failed to approve the order'
                status = Status.HTTP_400_BAD_REQUEST
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'Invalid Order'
            status = Status.HTTP_400_BAD_REQUEST
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = f'Key Error: {e}'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)

