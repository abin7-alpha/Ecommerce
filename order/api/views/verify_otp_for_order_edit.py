import sys
import traceback
import json

from datetime import datetime

from pytz import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist

from account.models import BasicUser, Retailer

from order.models import Order

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def verify_otp_for_order_edit(request):
    output = {}
    # data = json.loads(request.data)
    data = request.data
    retailer = None
    current_time = timezone('Asia/Kolkata').localize(datetime.now())

    try:
        mobile_number = data['phone']
        order_id = data['orderId']
        otp = data['otp']

        try:
            basic_user = BasicUser.objects.get(phone=mobile_number)
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
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'Please check mobile number'
            return Response(output, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            order_obj = Order.objects.get(id=order_id, retailer=retailer)
            if otp != basic_user.otp:
                output['status'] = 'failed'
                output['status_text'] = 'Otp verification failed please try again.'
                return Response(output, status=status.HTTP_400_BAD_REQUEST)
            output['status'] = "success"
            output['status_text'] = "Successfully verified the otp"
            output['order_id'] = order_obj.id
        except ObjectDoesNotExist:
            output['status']="failed"
            output['status_text']="No Matching Order found."
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
