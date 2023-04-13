import sys
import traceback
import json

from datetime import datetime

from pytz import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from account.models import BasicUser, Retailer

from order.models import Order

@api_view(['POST',])
@permission_classes([AllowAny,])
def verify_otp_for_retailer(request):
    output = {}
    data = request.data

    try:
        userName = data['userName']
        otp = data['otp']

        try:
            django_user = User.objects.get(username=userName)
            try:
                basic_user = BasicUser.objects.get(django_user=django_user)
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
                if otp != basic_user.otp:
                    output['status'] = 'failed'
                    output['status_text'] = 'Otp verification failed please try again.'
                    return Response(output, status=status.HTTP_400_BAD_REQUEST)
                output['status'] = "success"
                output['status_text'] = "Successfully verified the otp"
                return Response(output, status=status.HTTP_200_OK)
            except:
                output['status']="failed"
                output['status_text']="Invalid OTP"
            return Response(output, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            output['status'] = 'failed'
            output['status_text'] = 'No registered user found'
            return Response(output, status=status.HTTP_404_NOT_FOUND)
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status']='failed'
        output['status_text']=str(e[0])+": : Data is missing"
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        output['status']='failed'
        output['status_text']=str(e[0])+": : Data is missing"
    
    return Response(output, status=status.HTTP_400_BAD_REQUEST)
