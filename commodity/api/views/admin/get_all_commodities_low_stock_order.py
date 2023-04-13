import sys, traceback

from rest_framework import status as Status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.core.paginator import Paginator

from commodity.models import DcCommodity
from commodity.api.serializers.dc_commodity import DcCommodityForBatchSerializer

from account.decorators import is_logistics_manager


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@is_logistics_manager()
def get_all_low_stock_commodities(request):
    output = {}
    dc_id = request.query_params.get('dcId')
    page_number = request.query_params.get('pageNumber')
    
    try:
        commodities = DcCommodity.objects.filter(distribution_center=dc_id).order_by('available_quantity')

        p = Paginator(commodities, 20)
        current_page = p.page(int(page_number))

        commodity_serializer = DcCommodityForBatchSerializer(current_page.object_list, many=True)

        output['status'] = 'success'
        output['status_text'] = 'successfully fetched all the commodities'
        output['total_pages'] = p.num_pages
        output['current_page_number'] = current_page.number
        output['previous'] = current_page.has_previous()
        output['next'] = current_page.has_next()
        output['count'] = p.count
        output['results'] = commodity_serializer.data
        status = Status.HTTP_200_OK
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'failed to fetch the Commodities'
        status = Status.HTTP_404_NOT_FOUND

    return Response(output, status=status)