import sys, traceback

from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response

from commodity.models import DcCommodity
from commodity.api.serializers.dc_commodity import DcCommodityForBatchSerializer

from office.models import DistributionCenter

from django.db.models.functions import Cast
from django.db.models import FloatField, Q
from django.core.paginator import Paginator

@api_view(['GET',])
@permission_classes([IsAuthenticated])
def get_all_commodities_by_dc(request):
    output = {}

    try:
        dist_center_id = request.query_params.get('dcId')
        by_alphabetical_order = request.query_params.get('byALphabetical')
        page_number = request.query_params.get('pageNumber')
        try:
            distribution_center = DistributionCenter.objects.get(id=dist_center_id)
            try:
                commodities = None
                if by_alphabetical_order == 'true':
                    commodities = DcCommodity.objects.all().filter(is_active=True).filter(distribution_center=distribution_center).order_by('commodity__name')
                else:
                    commodities = DcCommodity.objects.annotate(mm_code_float=Cast('commodity__mm_code', output_field=FloatField())).filter(is_active=True).filter(distribution_center=distribution_center).order_by('mm_code_float').all()
                
                p = Paginator(commodities, 20)
                current_page = p.page(int(page_number))

                commodity_serializer = DcCommodityForBatchSerializer(current_page.object_list, many=True)

                output['status'] = 'success'
                output['status_txt'] = 'successfully fetched the commodities'
                output['total_pages'] = p.num_pages
                output['current_page_number'] = current_page.number
                output['previous'] = current_page.has_previous()
                output['next'] = current_page.has_next()
                output['count'] = p.count
                output['results'] = commodity_serializer.data
                return Response(output, status=status.HTTP_200_OK)
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_txt'] = 'Failed to fetch the commodities'
                return Response(output, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_txt'] = 'Invalid Distribution centre'
            return Response(output, status=status.HTTP_400_BAD_REQUEST)
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_txt'] = f'{e}, : key error'
        return Response(output, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET',])
@permission_classes([IsAuthenticated])
def search_commodities(request):
    output = {}

    try:
        dist_center_id = request.query_params.get('dcId')
        by_alphabetical_order = request.query_params.get('byALphabetical')
        page_number = request.query_params.get('pageNumber')
        search_key = request.query_params.get('searchKey')
        try:
            distribution_center = DistributionCenter.objects.get(id=dist_center_id)
            try:
                commodities = None
                if by_alphabetical_order == 'true':
                    commodities = DcCommodity.objects.all().filter(is_active=True).filter(distribution_center=distribution_center).order_by('commodity__name')
                else:
                    try:
                        drug_code = float(search_key)
                        commodities = DcCommodity.objects.annotate(mm_code_float=Cast('commodity__mm_code', output_field=FloatField())).filter(mm_code_float=str(drug_code)).filter(is_active=True).filter(distribution_center=distribution_center).order_by('mm_code_float').all()
                    except:
                        commodities = DcCommodity.objects.annotate(mm_code_float=Cast('commodity__mm_code', output_field=FloatField())).filter(Q(commodity__name__icontains=search_key) | Q(commodity__commodity_category__name__icontains=search_key) | Q(commodity__commodity_group__name__icontains=search_key)).filter(is_active=True).filter(distribution_center=distribution_center).order_by('mm_code_float').all()
                
                p = Paginator(commodities, 20)
                current_page = p.page(int(page_number))

                commodity_serializer = DcCommodityForBatchSerializer(current_page.object_list, many=True)

                output['status'] = 'success'
                output['status_txt'] = 'successfully fetched the commodities'
                output['total_pages'] = p.num_pages
                output['current_page_number'] = current_page.number
                output['previous'] = current_page.has_previous()
                output['next'] = current_page.has_next()
                output['count'] = p.count
                output['results'] = commodity_serializer.data
                return Response(output, status=status.HTTP_200_OK)
            except:
                traceback.print_exc(file=sys.stdout)
                output['status'] = 'failed'
                output['status_txt'] = 'Failed to fetch the commodities'
                return Response(output, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_txt'] = 'Invalid Distribution centre'
            return Response(output, status=status.HTTP_400_BAD_REQUEST)
    except KeyError as e:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_txt'] = f'{e}, : key error'
        return Response(output, status=status.HTTP_400_BAD_REQUEST)
    

class SetPagination(PageNumberPagination):
    page_size=15

class GetAllCommoditiesByDc(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = SetPagination
    serializer_class = DcCommodityForBatchSerializer
    def get_queryset(self):
        dist_center_id = self.request.query_params.get('dcId')
        by_alphabetical_order = self.request.query_params.get('byALphabetical')
        # page_number = self.request.query_params.get('pageNumber')
        distribution_center = DistributionCenter.objects.get(id=dist_center_id)

        queryset = None
        if by_alphabetical_order == 'true':
            queryset = DcCommodity.objects.all().filter(is_active=True).filter(distribution_center=distribution_center).order_by('commodity__name')
        else:
            queryset = DcCommodity.objects.annotate(mm_code_float=Cast('commodity__mm_code', output_field=FloatField())).filter(is_active=True).filter(distribution_center=distribution_center).order_by('mm_code_float').all()
        return queryset
