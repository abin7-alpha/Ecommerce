import json
import requests
import sys, traceback

from account.functions import url_encode
from janaushadi import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import ValidationError

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def get_access_using_refresh_token(request):
    output = {}
    data = request.data
    # print(request.data)
    # data = json.loads(request.data)
    print(data)

    try:
        refreshToken = data["refreshToken"]

        try:
            url = f"{settings.TOKEN_SERVER_URL}/o/token/"
            redirect_uri = 'dev.mahaveerdrugsplus.in'

            client_info = f'client_id={settings.CLIENT_ID}&client_secret={settings.CLIENT_SECRET}&grant_type=refresh_token'
            redirect_uri = f'&redirect_uri={url_encode(redirect_uri)}'
            refresh_token = f'&refresh_token={url_encode(refreshToken)}'
            payload = client_info + redirect_uri + refresh_token

            headers = {
                'Cache-Control': 'no-cache',
                'Content-Type': 'application/x-www-form-urlencoded',
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            data = json.loads(response.text)
            output['status'] = 'Success'
            output['status_text'] = 'Succesfully generated the accesstoken using refresh token'
            output.update(data)
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'Failed to get the accesstoken'
            return Response(output, status=status.HTTP_400_BAD_REQUEST)

    except ValidationError as error:
        output['status'] = 'failed'
        output['status_text'] = error
        return Response(output, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(output, status=status.HTTP_200_OK)
