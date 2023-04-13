import sys
import traceback
import json

from janaushadi import settings

from datetime import datetime

from pytz import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from account.models import BasicUser, Retailer
from account.functions import generate_OTP, send_mails, send_sms
from account.html_snippets import generated_otp_forgot_template, generate_otp_msg_forgot_template

from order.models import Order

@api_view(['POST'])
@permission_classes([AllowAny,])
def generate_otp_for_forgot_password(request):
    output = {}
    # data = json.loads(request.data)
    data = request.data
    retailer = None
    current_time = timezone('Asia/Kolkata').localize(datetime.now())

    try:
        # mobile_number = data['phone']
        # order_id = data['orderId']
        userEmail = data['userEmail']

        try:
            basic_user = BasicUser.objects.get(email=userEmail)

            try:
                retailer = Retailer.objects.get(user=basic_user)
                
                if retailer != None:
                    print("User mobile number = ", basic_user.phone)
                else:
                    output['status'] = 'failed'
                    output['status_text'] = 'No matching retailer found'
                    return Response(output, status=status.HTTP_404_NOT_FOUND)
            except ObjectDoesNotExist:
                output['status'] = 'failed'
                output['status_text'] = 'No registered user found'
                return Response(output, status=status.HTTP_404_NOT_FOUND)
            
            try:
                otp = generate_OTP(basic_user.phone)
                basic_user.otp = otp['OTP']
                basic_user.otp_creation_time = current_time
                basic_user.save()
                
                retailer_phone_number = basic_user.phone
                recipient = basic_user.email
                subject = "Mahaveer Drug House : Password Reset Request"
                body_text = (
                    "Hai! This is Mahaveer Drug House\r\n"
                )
                body_html = generated_otp_forgot_template.substitute(
                    otp=str(basic_user.otp),
                    app_name=settings.APP_NAME,
                    user_name=str(basic_user.name)
                )

                msg = generate_otp_msg_forgot_template.substitute(
                    otp=str(basic_user.otp),
                    app_name=settings.APP_NAME,
                    user_name=str(basic_user.name)
                )

                send_mails(recipient, body_html, body_text, subject)
                send_sms(msg, retailer_phone_number)

                output['status'] = "success"
                output['status_text'] = "OTP Generated Successsfully"
            except:
                traceback.print_exc(file=sys.stdout)
                output['status']="failed"
                output['status_text']="Failed to generate otp, internal server issue"
                return Response(output, status=status.HTTP_404_NOT_FOUND)
        except:
            output['status'] = 'failed'
            output['status_text'] = 'No matching retailer found'
            return Response(output, status=status.HTTP_404_NOT_FOUND)
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status']='failed'
        output['status_text']=str(e[0])+": : Data is missing"
    except ObjectDoesNotExist:
        output['status']="failed"
        output['status_text']="Retailer Object Doesn't Exist"
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        output['status']='failed'
        output['status_text']=str(e[0])+": : Data is missing"
    
    return Response(output)
