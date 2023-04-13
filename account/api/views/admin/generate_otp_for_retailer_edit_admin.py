import sys
import traceback

from janaushadi import settings

from datetime import datetime

from pytz import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist

from account.models import BasicUser, Retailer, Staff
from account.functions import generate_OTP, send_mails, send_sms
from account.html_snippets import generated_otp_forgot_admin_template, generate_otp_msg_forgot_admin_template
from account.decorators import is_retailer_manager

from order.models import Order

@api_view(['POST'])
@permission_classes([IsAuthenticated,])
@is_retailer_manager()
def generate_otp_for_retailer_edit_by_admin(request):
    output = {}
    # data = json.loads(request.data)
    data = request.data
    retailer = None
    current_time = timezone('Asia/Kolkata').localize(datetime.now())

    try:
        userEmail = data['userEmail']
        staff_id = data['staffId']

        try:
            basic_user = BasicUser.objects.get(email=userEmail)

            try:
                retailer = Retailer.objects.get(user=basic_user)
                
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
                output['status_text'] = 'No registered user found'
                return Response(output, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                staff = Staff.objects.get(id=staff_id)
                otp = generate_OTP(basic_user.phone)
                basic_user.otp = otp['OTP']
                basic_user.otp_creation_time = current_time
                basic_user.save()
                
                retailer_phone_number = f'91{basic_user.phone}'
                recipient = basic_user.email
                subject = "Mahaveer Drug House : Retailer Edit One Time Password By Mahaveer Staff"
                body_text = (
                    "Hai! This is Mahaveer Drug House\r\n"
                )
                body_html = generated_otp_forgot_admin_template.substitute(
                    otp=str(basic_user.otp),
                    app_name=settings.APP_NAME,
                    user_name=str(basic_user.name),
                    staff_name=str(staff.user.name)
                )

                msg = generate_otp_msg_forgot_admin_template.substitute(
                    otp=str(basic_user.otp),
                    app_name=settings.APP_NAME,
                    user_name=str(basic_user.name),
                    staff_name=str(staff.user.name)
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
