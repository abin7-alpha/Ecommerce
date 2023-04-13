import sys
import json
import traceback

from datetime import datetime

from pytz import timezone

from janaushadi import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist

from account.models import Retailer

from order.models import Order
from order.functions import increment_order_items_in_order, sendOrderConfirmationMailToCustomer
from order.functions import jsonOfOrderObjectAndOrderItemDetails, upload_invoice_to_aws, decrease_order_items_in_order

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def edit_order_items_in_order(request):
    # data = json.loads(request.data)
    data = request.data
    output = {}

    try:
        retailer_id = data['retailerId']
        order_id = data['orderId']
        edit_items = data['editItems']

        try:
            send_invoice_to_customer = settings.SEND_INVOICE_TO_CUSTOMER
        except KeyError:
            traceback.print_exc(file=sys.stdout)
            send_invoice_to_customer = True

        try:
            retailer = Retailer.objects.get(id=retailer_id)
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'Invalid retailer'
            return Response(output, status=status.HTTP_404_NOT_FOUND)
        
        try:
            order = Order.objects.filter(retailer=retailer).get(id=order_id)
            current_amount = order.amount
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'Ivalid order id'
            return Response(output, status=status.HTTP_404_NOT_FOUND)

        if retailer.is_payment_check_required:
            if edit_items['commodity_increment']:
                response, grand_total, is_partial_order_successful = increment_order_items_in_order(order, edit_items['commodity_increment'], 0, 0)
                output.update(response)

                order.amount = current_amount + grand_total
                order.save()

                print("New Grand Total:", order.amount)
                order.pending_amount = order.amount
                order.save()

                output['newSalesOrder'] = jsonOfOrderObjectAndOrderItemDetails(order)
                output['status']="success"
                output['status_text']="Order placement successfull."

                if is_partial_order_successful:
                    output['status']="success"
                    output['status_text']= "Order placement partially successfull. Please wait for the admin to get verfied"
                    output['status_msg'] = "There are some items is not in the stock, We will notify you when it arrives"
            
            if edit_items['commodity_decrement']:
                response, grand_total, is_partial_order_successful = increment_order_items_in_order(order, edit_items['commodity_increment'], 0, 0)
                output.update(response)

                order.amount = current_amount - grand_total
                order.save()

                print("New Grand Total:", order.amount)
                order.pending_amount = order.amount
                order.save()

                output['newSalesOrder'] = jsonOfOrderObjectAndOrderItemDetails(order)
                output['status']="success"
                output['status_text2']="Order placement successfull."
            
            out_file, response, is_send = sendOrderConfirmationMailToCustomer(order, send_invoice_to_customer)
            
            inv_url = upload_invoice_to_aws(out_file, destination=settings.COMPANY_NAME.replace(" ",""), object_name=(f"{order.id}" + ".pdf"))
            if inv_url:
                order.inv_url = inv_url
                order.save()
                output["invoice_url"] = inv_url

            return Response(output, status=status.HTTP_200_OK)
    except:
        output['status'] = 'failed'
        output['status_text'] = 'something went wrong please try again'
        return Response(output, status=status.HTTP_400_BAD_REQUEST)
   