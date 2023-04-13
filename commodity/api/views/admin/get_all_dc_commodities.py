import sys, traceback

from rest_framework import status as Status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.core.paginator import Paginator
from django.db.models.functions import Cast
from django.db.models import FloatField, Q

from commodity.models import DcCommodity
from commodity.api.serializers.dc_commodity import DcCommodityForBatchSerializer

from account.decorators import is_logistics_manager


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@is_logistics_manager()
def get_all_dc_commodities(request):
    output = {}
    dc_id = request.query_params.get('dcId')
    page_number = request.query_params.get('pageNumber')
    
    try:
        commodities = DcCommodity.objects.filter(distribution_center=dc_id).filter(is_active=True).filter(is_janaushadi=False).order_by('created')

        p = Paginator(commodities, 50)
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@is_logistics_manager()
def get_all_inactive_dc_commodities(request):
    output = {}
    dc_id = request.query_params.get('dcId')
    page_number = request.query_params.get('pageNumber')
    
    try:
        commodities = DcCommodity.objects.filter(distribution_center=dc_id).filter(is_active=False).filter(is_janaushadi=False).order_by('created')

        p = Paginator(commodities, 50)
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@is_logistics_manager()
def search_dc_commodities(request):
    output = {}
    dc_id = request.query_params.get('dcId')
    page_number = request.query_params.get('pageNumber')
    search_key = request.query_params.get('searchKey')
    
    try:
        try:
            try:
                commodities = DcCommodity.objects.annotate(mm_code_float=Cast('commodity__mm_code', output_field=FloatField())).filter(is_active=True).filter(is_janaushadi=False).filter(id=int(search_key)).filter(distribution_center=dc_id).order_by('mm_code_float').all()
                if commodities:
                    pass
                else:
                    raise Exception
            except:
                drug_code = float(search_key)
                commodities = DcCommodity.objects.annotate(mm_code_float=Cast('commodity__mm_code', output_field=FloatField())).filter(is_active=True).filter(is_janaushadi=False).filter(mm_code_float=str(drug_code)).filter(distribution_center=dc_id).order_by('mm_code_float').all()
        except:
            commodities = DcCommodity.objects.annotate(mm_code_float=Cast('commodity__mm_code', output_field=FloatField())).filter(is_active=True).filter(is_janaushadi=False).filter(Q(commodity__name__icontains=search_key) | Q(commodity__commodity_category__name__icontains=search_key) | Q(commodity__commodity_group__name__icontains=search_key)).filter(distribution_center=dc_id).order_by('mm_code_float').all()

        p = Paginator(commodities, 50)
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@is_logistics_manager()
def search_in_active_dc_commodities(request):
    output = {}
    dc_id = request.query_params.get('dcId')
    page_number = request.query_params.get('pageNumber')
    search_key = request.query_params.get('searchKey')
    
    try:
        try:
            try:
                commodities = DcCommodity.objects.annotate(mm_code_float=Cast('commodity__mm_code', output_field=FloatField())).filter(is_active=False).filter(is_janaushadi=False).filter(id=int(search_key)).filter(distribution_center=dc_id).order_by('mm_code_float').all()
                if commodities:
                    pass
                else:
                    raise Exception
            except:
                drug_code = float(search_key)
                commodities = DcCommodity.objects.annotate(mm_code_float=Cast('commodity__mm_code', output_field=FloatField())).filter(is_active=False).filter(is_janaushadi=False).filter(mm_code_float=str(drug_code)).filter(distribution_center=dc_id).order_by('mm_code_float').all()
        except:
            commodities = DcCommodity.objects.annotate(mm_code_float=Cast('commodity__mm_code', output_field=FloatField())).filter(is_active=False).filter(is_janaushadi=False).filter(Q(commodity__name__icontains=search_key) | Q(commodity__commodity_category__name__icontains=search_key) | Q(commodity__commodity_group__name__icontains=search_key)).filter(distribution_center=dc_id).order_by('mm_code_float').all()

        p = Paginator(commodities, 50)
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@is_logistics_manager()
def get_all_dc_commodities_non_janaushadi(request):
    output = {}
    dc_id = request.query_params.get('dcId')
    page_number = request.query_params.get('pageNumber')
    
    try:
        commodities = DcCommodity.objects.filter(distribution_center=dc_id).filter(is_active=True).filter(is_janaushadi=True).order_by('created')

        p = Paginator(commodities, 50)
        current_page = p.page(int(page_number))

        commodity_serializer = DcCommodityForBatchSerializer(current_page.object_list, many=True)

        output['status'] = 'success'
        output['status_text'] = 'successfully fetched all the commodities non janaushadi'
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
@is_logistics_manager()
def get_all_inactive_dc_commodities_non_janaushadi(request):
    output = {}
    dc_id = request.query_params.get('dcId')
    page_number = request.query_params.get('pageNumber')
    
    try:
        commodities = DcCommodity.objects.filter(distribution_center=dc_id).filter(is_active=False).filter(is_janaushadi=True).order_by('created')

        p = Paginator(commodities, 50)
        current_page = p.page(int(page_number))

        commodity_serializer = DcCommodityForBatchSerializer(current_page.object_list, many=True)

        output['status'] = 'success'
        output['status_text'] = 'successfully fetched all the in-active commodities non janaushadi'
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
        output['status_text'] = 'failed to fetch in-active commodities non janaushadi'
        status = Status.HTTP_404_NOT_FOUND

    return Response(output, status=status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@is_logistics_manager()
def search_dc_commodities_non_janaushadi(request):
    output = {}
    dc_id = request.query_params.get('dcId')
    page_number = request.query_params.get('pageNumber')
    search_key = request.query_params.get('searchKey')
    
    try:
        try:
            try:
                commodities = DcCommodity.objects.annotate(mm_code_float=Cast('commodity__mm_code', output_field=FloatField())).filter(is_active=True).filter(is_janaushadi=True).filter(id=int(search_key)).filter(distribution_center=dc_id).order_by('mm_code_float').all()
                if commodities:
                    pass
                else:
                    raise Exception
            except:
                drug_code = float(search_key)
                commodities = DcCommodity.objects.annotate(mm_code_float=Cast('commodity__mm_code', output_field=FloatField())).filter(is_active=True).filter(is_janaushadi=True).filter(mm_code_float=str(drug_code)).filter(distribution_center=dc_id).order_by('mm_code_float').all()
        except:
            commodities = DcCommodity.objects.annotate(mm_code_float=Cast('commodity__mm_code', output_field=FloatField())).filter(is_active=True).filter(is_janaushadi=True).filter(Q(commodity__name__icontains=search_key) | Q(commodity__commodity_category__name__icontains=search_key) | Q(commodity__commodity_group__name__icontains=search_key)).filter(distribution_center=dc_id).order_by('mm_code_float').all()

        p = Paginator(commodities, 50)
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@is_logistics_manager()
def search_inactive_dc_commodities_non_janaushadi(request):
    output = {}
    dc_id = request.query_params.get('dcId')
    page_number = request.query_params.get('pageNumber')
    search_key = request.query_params.get('searchKey')
    
    try:
        try:
            try:
                commodities = DcCommodity.objects.annotate(mm_code_float=Cast('commodity__mm_code', output_field=FloatField())).filter(is_active=False).filter(is_janaushadi=True).filter(id=int(search_key)).filter(distribution_center=dc_id).order_by('mm_code_float').all()
                if commodities:
                    pass
                else:
                    raise Exception
            except:
                drug_code = float(search_key)
                commodities = DcCommodity.objects.annotate(mm_code_float=Cast('commodity__mm_code', output_field=FloatField())).filter(is_active=False).filter(is_janaushadi=True).filter(mm_code_float=str(drug_code)).filter(distribution_center=dc_id).order_by('mm_code_float').all()
        except:
            commodities = DcCommodity.objects.annotate(mm_code_float=Cast('commodity__mm_code', output_field=FloatField())).filter(is_active=False).filter(is_janaushadi=True).filter(Q(commodity__name__icontains=search_key) | Q(commodity__commodity_category__name__icontains=search_key) | Q(commodity__commodity_group__name__icontains=search_key)).filter(distribution_center=dc_id).order_by('mm_code_float').all()

        p = Paginator(commodities, 50)
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

# class SetPagination(PageNumberPagination):
#     page_size=50

# class get_all_dc_commodities(ListAPIView):
#     permission_classes = (IsAuthenticated,)
#     pagination_class = SetPagination
#     serializer_class = DcCommodityForBatchSerializer
#     def get_queryset(self):
#         dc_id = self.request.query_params.get('dcId')
#         queryset = DcCommodity.objects.filter(distribution_center=dc_id).order_by('created')
#         return queryset
