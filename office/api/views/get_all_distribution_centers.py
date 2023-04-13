import sys, traceback

from rest_framework import status as Status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from office.models import DistributionCenter
from office.api.serializers.distribution_center import DistributionCenterSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_distribution_centers(request):
    output = {}

    try:
        distribution_centers = DistributionCenter.objects.all()
        # for i in distribution_centers:
        #     print(i)
        distribution_center_serializer = DistributionCenterSerializer(distribution_centers, many=True)
        output['status'] = 'success'
        output['status_text'] = 'successfully fetched all the distribution centers'
        output['distribution_centers'] = distribution_center_serializer.data
        status = Status.HTTP_200_OK
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'failed to fetch the distrbution centers'
        status = Status.HTTP_404_NOT_FOUND

    return Response(output, status=status)
