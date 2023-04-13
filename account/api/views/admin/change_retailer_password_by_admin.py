import sys
import traceback

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist

from account.models import BasicUser, Retailer
from account.decorators import is_retailer_manager

@api_view(['POST',])
@permission_classes([AllowAny,])
@is_retailer_manager()
def verify_otp_and_change_user_password(request):
    output = {}
    data = request.data

    try:
        userEmail = data['userEmail']
        newPassword = data['newPassword']
        otp = str(data['otp'])

        try:
            basic_user = BasicUser.objects.get(email=userEmail)

            try:
                retailer = Retailer.objects.get(user=basic_user)
                
                if retailer != None:
                    print("User mobile number = ", basic_user.phone)
                else:
                    output['status'] = 'failed'
                    output['status_text'] = 'No matching retailer found'
                    return Response(output, status=status.HTTP_401_UNAUTHORIZED)
            except ObjectDoesNotExist:
                output['status'] = 'failed'
                output['status_text'] = 'No registered user found'
                return Response(output, status=status.HTTP_401_UNAUTHORIZED)
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
                django_user = basic_user.django_user
                django_user.set_password(newPassword)
                django_user.save()
                output['status'] = "success"
                output['status_text'] = "Successfully changed the password"
                return Response(output, status=status.HTTP_200_OK)
            except:
                output['status']="failed"
                output['status_text']="Invalid OTP"
            return Response(output, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            output['status'] = 'failed'
            output['status_text'] = 'No registered user found'
            return Response(output, status=status.HTTP_400_BAD_REQUEST)
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status']='failed'
        output['status_text']= f'{e}' + ": : Data is missing"
        return Response(output, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        output['status']='failed'
        output['status_text']= f'{e}' + ": : Data is missing"
        return Response(output, status=status.HTTP_400_BAD_REQUEST)
    