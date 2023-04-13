import sys
import traceback

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status as Status

from django.core.exceptions import ObjectDoesNotExist

from account.models import Retailer
from account.decorators import is_retailer_manager

@api_view(['POST',])
@permission_classes([AllowAny,])
@is_retailer_manager()
def retailer_edit_by_admin(request):
    output = {}
    data = request.data

    try:
        retailer_id = data['retailerId']
        otp = str(data['otp'])

        try:
            retailer = Retailer.objects.get(id=retailer_id)
            print(retailer)

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
                
                try:
                    name = data['name']
                    basic_user.name = name
                    basic_user.save()
                    output['status'] = "success"
                    output['status_text'] = "Successfully changed the password"
                    return Response(output, status=Status.HTTP_200_OK)
                except:
                    output['status'] = 'failed'
                    output['status_text'] = 'Failed to update the criteria'
                    status = Status.HTTP_400_BAD_REQUEST

                try:
                    secondary_phone = str(data['secondaryPhone'])
                    basic_user.secondary_phone = secondary_phone
                    basic_user.save()
                    output['status'] = "success"
                    output['status_text'] = "Successfully updated the retailer secondary phone number"
                    return Response(output, status=Status.HTTP_200_OK)
                except:
                    output['status'] = 'failed'
                    output['status_text'] = 'Failed to update the criteria'
                    status = Status.HTTP_400_BAD_REQUEST

                try:
                    email = data['email']
                    basic_user.email = email
                    basic_user.save()
                    output['status'] = "success"
                    output['status_text'] = "Successfully updated the retailer email"
                    return Response(output, status=Status.HTTP_200_OK)
                except:
                    output['status'] = 'failed'
                    output['status_text'] = 'Failed to update the criteria'
                    status = Status.HTTP_400_BAD_REQUEST

                try:
                    phone = str(data['phone'])
                    basic_user.phone = phone
                    basic_user.save()
                    output['status'] = "success"
                    output['status_text'] = "Successfully updated the phone number"
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