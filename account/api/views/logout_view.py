from django.contrib.auth import logout

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST',])
@permission_classes([IsAuthenticated])
def logout_user(request):
    output = {}

    try:
        logout(request)
        output['status'] = 'success'
        output['status_txt'] = 'successfully logged out the user.'
        return Response(output, status=status.HTTP_200_OK)
    except:
        output['status'] = 'failed'
        output['status_txt'] = 'failed to logged out the user, something went wrong'
        return Response(output, status=status.HTTP_400_BAD_REQUEST)
