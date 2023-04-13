import sys
import traceback
import asyncio

from janaushadi import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status as Status

from django.core.exceptions import ObjectDoesNotExist

from order.models import Order, OrderItem
from order.api.serializers.order_item import OrderItemSerializer
from order.api.serializers.order import OrderSerializerForDetails
from order.functions import upload_invoice_to_aws, send_updated_order_sms, sendUpdatedOrderConfirmationMailToCustomer

from account.functions import stock_available_send_notification

@api_view(['POST',])
@permission_classes([AllowAny,])
def retailer_order_remove_batch_by_admin(request):
    output = {}
    data = request.data

    try:
        order_id = data['orderId']
        order_item_id = data['orderItemId']
        otp = str(data['otp'])
        quantity = data['quantity']

        try:
            order = Order.objects.get(id=order_id)
            retailer = order.retailer

            try:
                basic_user = retailer.user
                if retailer != None:
                    print("User mobile number = ", basic_user.phone)
                else:
                    output['status'] = 'failed'
                    output['status_text'] = 'No matching retailer found'
                    return Response(output, status=Status.HTTP_401_UNAUTHORIZED)
            except ObjectDoesNotExist:
                output['status'] = 'failed'
                output['status_text'] = 'No registered user found'
                return Response(output, status=Status.HTTP_401_UNAUTHORIZED)
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Please check mobile number'
                return Response(output, status=Status.HTTP_400_BAD_REQUEST)
            
            try:
                if otp != basic_user.otp:
                    output['status'] = 'failed'
                    output['status_text'] = 'Otp verification failed please try again.'
                    return Response(output, status=Status.HTTP_400_BAD_REQUEST)
                
                if order.status != 'New':
                    output['status'] = 'failed'
                    output['status_text'] = 'This order is not editable as its already procesed'
                    return Response(output, status=Status.HTTP_400_BAD_REQUEST)
                
                try:
                    order_item = OrderItem.objects.get(id=order_item_id)
                    current_order_item_quantity = order_item.quantity
                    current_total_product_price = round(order_item.price+(order_item.price * (order_item.commodity.commodity.gst / 100)), 2)
                    current_total_quantity_price = current_total_product_price * order_item.quantity
                    order_item.quantity = quantity
                    order_item.save()

                    dc_commodity = order_item.commodity
                    dc_commodity_available_quantity = dc_commodity.available_quantity
                    dc_commodity.available_quantity -= current_order_item_quantity
                    dc_commodity.save()
                    dc_commodity.available_quantity += order_item.quantity
                    dc_commodity.save()

                    commodity_batch = order_item.commodity_batch
                    commodity_batch.available_quantity -= current_order_item_quantity
                    commodity_batch.save()
                    commodity_batch.available_quantity += order_item.quantity
                    commodity_batch.save()

                    price = commodity_batch.price
                    order_item.delivery_charge = 0
                    order_item_sgst = round((float(price * order_item.quantity) * order_item.commodity.commodity.gst/ 200), 4)
                    order_item_cgst = round((float(price * order_item.quantity) * order_item.commodity.commodity.gst/ 200), 4)
                    order_item.sgst = order_item_sgst
                    order_item.cgst = order_item_cgst
                    order_item.save()
                    total_product_price = round(order_item.price+(order_item.price * (order_item.commodity.commodity.gst / 100)), 2)
                    total_quantity_price = total_product_price * order_item.quantity

                    # current_order_pending_amount = order.pending_amount
                    # current_order_amount = order.amount
                    order.amount -= current_total_quantity_price
                    order.pending_amount -= current_total_quantity_price
                    order.save()
                    order.amount += total_quantity_price
                    order.pending_amount += total_quantity_price
                    order.save()

                    try:
                        send_invoice_to_customer = settings.SEND_INVOICE_TO_CUSTOMER
                    except KeyError:
                        traceback.print_exc(file=sys.stdout)
                        send_invoice_to_customer = True

                    out_file, response, is_send = sendUpdatedOrderConfirmationMailToCustomer(order, send_invoice_to_customer)
			
                    inv_url = upload_invoice_to_aws(out_file, destination=settings.COMPANY_NAME.replace(" ",""), object_name=(f"{order.id}" + ".pdf"))
                    if inv_url:
                        order.inv_url = inv_url
                        order.save()
                        output["invoice_url"] = inv_url
                        send_updated_order_sms(retailer, order, inv_url)

                    if dc_commodity.available_quantity > dc_commodity_available_quantity:
                        stock_available_send_notification(dc_commodity)

                    output['status'] = "success"
                    output['status_text'] = "Successfully updated the quantity"
                    output['editedOrder'] = OrderSerializerForDetails(order).data
                    output['editedOrderItem'] = OrderItemSerializer(order_item).data

                    order_item.delete()

                    return Response(output, status=Status.HTTP_200_OK)
                except:
                    output['status'] = 'failed'
                    output['status_text'] = 'Failed to update the criteria'
                    status = Status.HTTP_400_BAD_REQUEST

                return Response(output, status=status)
            except:
                output['status']="failed"
                output['status_text']="Invalid OTP"
            return Response(output, status=Status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            output['status'] = 'failed'
            output['status_text'] = 'No registered user found'
            return Response(output, status=Status.HTTP_400_BAD_REQUEST)
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status']='failed'
        output['status_text']= f'{e}' + ": : Data is missing"
        return Response(output, status=Status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        output['status']='failed'
        output['status_text']= f'{e}' + ": : Data is missing"
        return Response(output, status=Status.HTTP_400_BAD_REQUEST)
    