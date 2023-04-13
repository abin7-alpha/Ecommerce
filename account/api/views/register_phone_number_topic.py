import sys, traceback
import boto3

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status as Status
from rest_framework.response import Response

from janaushadi import settings

@api_view(['GET',])
@permission_classes([AllowAny,])
def register_phone_number_to_topic(request):
    output = {}
    if request.method == "GET":
        try:
            number = request.GET['number']
            print(number)
            number = '+'+number.strip()
            print(number)
            # validate phone number
            # if not re.match(r'^\+(?:[0-9]\x20?){6,14}[0-9]$',number):
            #     raise Exception("number_invalid")
            client = boto3.client(
                'sns',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.SNS_REGION
            )
            
            response = client.create_sms_sandbox_phone_number(
                PhoneNumber=number,
                LanguageCode='en-US'
            )
            print(response)
        except Exception as e:
            print("Exception4:", e)
            output["message"] = "exception raised"
            output["error"] = str(e)
            status = Status.HTTP_400_BAD_REQUEST
        else:
            output["message"] = "Make a request ot the verification url along with otp"
            # output["verification-url"]=url
            output["status"] = "success"
            status = Status.HTTP_200_OK
    else:
        output["message"] = "bag requestm Use method GET"
        output["status"] = "failed"
        status = Status.HTTP_400_BAD_REQUEST
    return Response(output, status=status)

@api_view(['GET',])
@permission_classes([AllowAny,])
def verify_sanbox_number(request):
    output = {}

    if request.method == "GET":
        try:
            number = request.GET["number"]
            otp = request.GET["otp"]
            number = '+'+number.strip()
            # if not re.match(r'^\+(?:[0-9]\x20?){6,14}[0-9]$',number):
            #     raise Exception("number_invalid")
            client = boto3.client(
                'sns',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.SNS_REGION
            )
            response = client.verify_sms_sandbox_phone_number(
                PhoneNumber=number,
                OneTimePassword=otp
            )
            print(response)
            response = client.subscribe(
                TopicArn='arn:aws:sns:ap-south-1:564925070387:MahaveerDrugsPlus',
                # arn:aws:sns:ap-south-1:392333643268:VSSTEST
                Protocol='sms',
                Endpoint=number,
                ReturnSubscriptionArn=False
            )
        except Exception as e:
            print("Exception4:", e)
            traceback.print_exc(file=sys.stdout)
            output["message"] = "exception raised"
            output["error"] = str(e)
            status = Status.HTTP_400_BAD_REQUEST
        else:
            output["status"] = "success"
            status = Status.HTTP_200_OK
    else:

        output["message"] = "bag requestm Use method GET"
        output["status"] = "failed"
        status = Status.HTTP_400_BAD_REQUEST
    return Response(output, status=status)
