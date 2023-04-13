import sys, traceback

from rest_framework import status as Status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.core.paginator import Paginator
from django.db.models.functions import Cast
from django.db.models import FloatField, Q

from commodity.models import Commodity
from commodity.api.serializers.commodity import CommoditySerializer

from account.decorators import is_logistics_manager


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@is_logistics_manager()
def get_all_commodities(request):
    output = {}
    page_number = request.query_params.get('pageNumber')

    try:
        commodities = Commodity.objects.filter(is_active=True).all()

        p = Paginator(commodities, 50)
        current_page = p.page(int(page_number))

        commodity_serializer = CommoditySerializer(current_page.object_list, many=True)
        
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_all_commodities(request):
    output = {}
    page_number = request.query_params.get('pageNumber')
    search_key = request.query_params.get('searchKey')

    try:
        try:
            try:
                commodities = Commodity.objects.annotate(mm_code_float=Cast('mm_code', output_field=FloatField())).filter(is_active=True).filter(id=int(search_key)).order_by('mm_code_float').all()
                if commodities:
                    pass
                else:
                    raise Exception
            except:
                drug_code = float(search_key)
                commodities = Commodity.objects.annotate(mm_code_float=Cast('mm_code', output_field=FloatField())).filter(is_active=True).filter(mm_code_float=str(drug_code)).order_by('mm_code_float').all()
        except:
            commodities = Commodity.objects.annotate(mm_code_float=Cast('mm_code', output_field=FloatField())).filter(is_active=True).filter(Q(name__icontains=search_key) | Q(commodity_category__name__icontains=search_key) | Q(commodity_group__name__icontains=search_key)).order_by('mm_code_float').all()

        p = Paginator(commodities, 50)
        current_page = p.page(int(page_number))

        commodity_serializer = CommoditySerializer(current_page.object_list, many=True)
        
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_inactive_commodities(request):
    output = {}
    page_number = request.query_params.get('pageNumber')

    try:
        commodities = Commodity.objects.filter(is_active=False).all()

        p = Paginator(commodities, 50)
        current_page = p.page(int(page_number))

        commodity_serializer = CommoditySerializer(current_page.object_list, many=True)
        
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_inactive_commodities(request):
    output = {}
    page_number = request.query_params.get('pageNumber')
    search_key = request.query_params.get('searchKey')

    try:
        try:
            try:
                commodities = Commodity.objects.annotate(mm_code_float=Cast('mm_code', output_field=FloatField())).filter(is_active=False).filter(id=int(search_key)).order_by('mm_code_float').all()
                if commodities:
                    pass
                else:
                    raise Exception
            except:
                drug_code = float(search_key)
                commodities = Commodity.objects.annotate(mm_code_float=Cast('mm_code', output_field=FloatField())).filter(is_active=False).filter(mm_code_float=str(drug_code)).order_by('mm_code_float').all()
        except:
            commodities = Commodity.objects.annotate(mm_code_float=Cast('mm_code', output_field=FloatField())).filter(is_active=False).filter(Q(name__icontains=search_key) | Q(commodity_category__name__icontains=search_key) | Q(commodity_group__name__icontains=search_key)).order_by('mm_code_float').all()

        p = Paginator(commodities, 50)
        current_page = p.page(int(page_number))

        commodity_serializer = CommoditySerializer(current_page.object_list, many=True)
        
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

# class SetPagination(PageNumberPagination):
#     page_size=50

# class get_all_commodities(ListAPIView):
#     permission_classes = (IsAuthenticated,)
#     pagination_class = SetPagination
#     serializer_class = CommoditySerializer
#     def get_queryset(self):
#         queryset = Commodity.objects.all().order_by('-created')
#         return queryset
    