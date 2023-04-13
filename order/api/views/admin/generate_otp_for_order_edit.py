import sys
import traceback
import json

from janaushadi import settings

from datetime import datetime

from pytz import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist

from account.models import Staff
from account.functions import generate_OTP, send_mails, send_sms

from order.models import Order
from order.html_snippets import generated_otp_retailer_order_admin_edit_template, generate_otp_msg_retailer_order_edit_admin_template

@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def generate_otp_for_retailer_order_edit_by_admin(request):
    output = {}
    # data = json.loads(request.data)
    data = request.data
    retailer = None
    current_time = timezone('Asia/Kolkata').localize(datetime.now())

    try:
        order_id = data['orderId']
        staff_id = data['staffId']

        try:
            order = Order.objects.get(id=order_id)

            try:
                retailer = order.retailer
                basic_user = retailer.user
                
                if retailer != None:
                    print("User mobile number = ", basic_user.phone)
                else:
                    traceback.print_exc(file=sys.stdout)
                    output['status'] = 'failed'
                    output['status_text'] = 'No matching retailer found'
                    return Response(output, status=status.HTTP_401_UNAUTHORIZED)
            except ObjectDoesNotExist:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_text'] = 'Invalid Order'
                return Response(output, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                staff = Staff.objects.get(id=staff_id)
                otp = generate_OTP(basic_user.phone)
                basic_user.otp = otp['OTP']
                basic_user.otp_creation_time = current_time
                basic_user.save()
                
                retailer_phone_number = f'91{basic_user.phone}'
                recipient = basic_user.email
                subject = "Mahaveer Drug House : Retailer Order Edit One Time Password By Mahaveer Staff"
                body_text = (
                    "Hai! This is Mahaveer Drug House\r\n"
                )
                body_html = generated_otp_retailer_order_admin_edit_template.substitute(
                    otp=str(basic_user.otp),
                    app_name=settings.APP_NAME,
                    user_name=str(basic_user.name),
                    staff_name=str(staff.user.name),
                    order_no=str(order.order_no)
                )

                msg = generate_otp_msg_retailer_order_edit_admin_template.substitute(
                    otp=str(basic_user.otp),
                    app_name=settings.APP_NAME,
                    user_name=str(basic_user.name),
                    staff_name=str(staff.user.name),
                    order_no=str(order.order_no)
                )

                send_mails(recipient, body_html, body_text, subject)
                send_sms(msg, retailer_phone_number)

                output['status'] = "success"
                output['status_text'] = "OTP Generated Successsfully"
            except:
                traceback.print_exc(file=sys.stdout)
                output['status']="failed"
                output['status_text']="Failed to generate otp, internal server issue"
                return Response(output, status=status.HTTP_400_BAD_REQUEST)
        except:
            output['status'] = 'failed'
            output['status_text'] = 'No matching retailer found'
            return Response(output, status=status.HTTP_401_UNAUTHORIZED)
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status']='failed'
        output['status_text']= f"{e} " + ": : Data is missing"
    except ObjectDoesNotExist:
        output['status']="failed"
        output['status_text']="Retailer Object Doesn't Exist"
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        output['status']='failed'
        output['status_text']= f"{e}" + ": : Data is missing"
    
    return Response(output, status=status.HTTP_200_OK)

