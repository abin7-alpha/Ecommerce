import json
import traceback, sys

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from account.functions import get_token
from account.models import BasicUser, Retailer
from account.api.serializers.retailer_serializer import RetailerSerializer

# @method_decorator(ensure_csrf_cookie, name='dispatch')
# class GetCSRFToken(APIView):
#     permission_classes = (AllowAny, )

#     def get(self, request, format=None):
#         return Response({ 'success': 'CSRF cookie set' })

@api_view(['POST',])
@permission_classes([AllowAny,])
def login_user(request):
    # data = request.data
    data = json.loads(request.data)
    output = {}

    username = data['userName']
    password = data['password']

    try:
        user = User.objects.get(username=username)
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = "failed"
        output['status_text'] = "Account not exists"
        return Response(output, status=status.HTTP_404_NOT_FOUND)
    
    try:
        basic_user = BasicUser.objects.get(django_user=user)
        retailer = Retailer.objects.get(user=basic_user)
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = "failed"
        output['status_text'] = "You dont have permission to authorize with this credentials"
        return Response(output, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        if basic_user.is_active:
            pass
        else:
            raise Exception
    except:
        output['status'] = "failed"
        output['status_text'] = "Your account has been inactive, contact admin"
        return Response(output, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        try:
            authorized_user = authenticate(request, username=username, password=password)
            
            if authorized_user == None:
                raise Exception
        except:
            output['status'] = "failed"
            output['status_text'] = "Incorrect password"
            return Response(output, status=status.HTTP_401_UNAUTHORIZED)
        
        redirect_uri = 'http://127.0.0.1:8000/'
        token = get_token(username, password, redirect_uri)
        retailer_serializer = RetailerSerializer(retailer)
        output['status'] = 'success'
        output["status_text"] = "Succesfully Auntheticated"
        output["email"] = user.email
        output["user_name"] = user.username
        output['retailer'] = retailer_serializer.data
        output.update(token)
        return Response(output, status=status.HTTP_200_OK)
    except Exception as error:
        traceback.print_exc(file=sys.stdout)
        output['status'] = "failed"
        output['status_text'] = "Failed to login"
        return Response(output, status=status.HTTP_400_BAD_REQUEST)
