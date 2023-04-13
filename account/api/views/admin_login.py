import json
import traceback, sys

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from account.functions import get_token
from account.models import Staff, BasicUser

from janaushadi import settings

@api_view(['POST',])
@permission_classes([AllowAny,])
def login_admin(request):
    data = request.data
    # data = json.loads(request.data)
    output = {}

    username = data['userName']
    password = data['password']

    try:
        user = User.objects.get(username=username)
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = "failed"
        output['status_text'] = "Account not exists"
        return Response(output, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        basic_user = BasicUser.objects.get(django_user=user)
        staff = Staff.objects.get(user=basic_user)
    except:
        output['status'] = "failed"
        output['status_text'] = "Dont have permision to access this functionality"
        return Response(output, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        try:
            authorized_user = authenticate(request, username=username, password=password)
            
            if authorized_user == None:
                raise Exception
        except:
            output['status'] = "failed"
            output['status_text'] = "Incorrect password"
            return Response(output, status=status.HTTP_401_UNAUTHORIZED)
        
        redirect_uri = settings.REDIRECT_URL
        token = get_token(username, password, redirect_uri)
        print(token)
        output['status'] = 'success'
        output["status_text"] = "Succesfully Auntheticated"
        output["email"] = user.email
        output['user_id'] = staff.id
        output["user_name"] = user.username
        output["user_type"] = "Admin"
        output.update(token)
        return Response(output, status=status.HTTP_200_OK)
    except Exception as error:
        traceback.print_exc(file=sys.stdout)
        output['status'] = "failed"
        output['status_text'] = "Failed to login"
        return Response(output, status=status.HTTP_400_BAD_REQUEST)
    