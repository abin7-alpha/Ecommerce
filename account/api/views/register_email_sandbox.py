import sys, traceback
import boto3
import re

from rest_framework.response import Response
from rest_framework import status as Status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from janaushadi import settings

def check_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        return True

    else:
        return False

@api_view(['POST',])
@permission_classes([AllowAny,])
def register_email_to_sandbox(request):
    output = {}
    if request.method == "POST":
        try:

            emailId = request.data['emailId']
            print(emailId)
            # validate email Id
            if not check_email(emailId):
                raise Exception("email id not valid")
            client = boto3.client(
                'ses',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.SNS_REGION
            )
            response = client.verify_email_identity(
                EmailAddress=emailId
            )
            print(response)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            print("Exception4:", e)
            output["message"] = "exception raised"
            output["error"] = str(e)
            status = Status.HTTP_400_BAD_REQUEST
        else:
            output["status"] = "success"
            status = Status.HTTP_200_OK
            output["message"] = "verification mail send to emailId"
    else:
        output["message"] = "bag requestm Use method GET"
        output["status"] = "failed"
        status = Status.HTTP_400_BAD_REQUEST
    return Response(output, status)
