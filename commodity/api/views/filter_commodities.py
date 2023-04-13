from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from commodity.models import DcCommodity
from commodity.api.serializers.dc_commodity import DcCommodityForBatchSerializer

from office.models import DistributionCenter

class CommoditiesAlphabeticalOrderAllList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    serializer_class = DcCommodityForBatchSerializer
    def get_queryset(self):
        dc_id = self.request.query_params.get('dcId')
        dc = DistributionCenter.objects.get(id=str(dc_id))
        queryset = DcCommodity.objects.all().filter(is_active=True).filter(distribution_center=dc).order_by('commodity__name')
        return queryset

class CommoditiesAlphabeticalOrderList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    serializer_class = DcCommodityForBatchSerializer

    def get_queryset(self):
        dc_id = self.request.query_params.get('dcId')
        dc = DistributionCenter.objects.get(id=str(dc_id))
        letter = self.request.query_params.get('letter')
        if letter:
            queryset = DcCommodity.objects.all().order_by('commodity__name').filter(distribution_center=dc).filter(is_active=True).filter(Q(commodity__name__startswith=letter)|Q(commodity__name__startswith=letter.upper()))
        else:
            queryset = DcCommodity.objects.all().filter(distribution_center=dc)
        return queryset
    
class CommoditiesAlphabeticalOrderSimilarProductsList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    serializer_class = DcCommodityForBatchSerializer

    def get_queryset(self):
        dc_id = self.request.query_params.get('dcId')
        dc = DistributionCenter.objects.get(id=str(dc_id))
        letter = self.request.query_params.get('letter')
        commodity_id = self.request.query_params.get('comId')
        queryset = DcCommodity.objects.all().order_by('commodity__name').filter(distribution_center=dc).filter(is_active=True).filter(Q(commodity__name__startswith=letter)|Q(commodity__name__startswith=letter.upper())).exclude(id=commodity_id)
        return queryset
    
class CommoditiesDrugCodeOrder(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    serializer_class = DcCommodityForBatchSerializer

    def get_queryset(self):
        dc_id = self.request.query_params.get('dcId')
        dc = DistributionCenter.objects.get(id=str(dc_id))
        queryset = DcCommodity.objects.all().order_by('commodity__mm_code').filter(is_active=True).filter(distribution_center=dc)
        return queryset


class CommoditiesDrugCodeOrderSimilarProductsList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    # queryset = DcCommodity.objects.all().order_by('commodity__mm_code').filter(is_active=True)
    serializer_class = DcCommodityForBatchSerializer

    def get_queryset(self):
        dc_id = self.request.query_params.get('dcId')
        dc = DistributionCenter.objects.get(id=str(dc_id))
        commodity_id = self.request.query_params.get('comId')
        queryset = DcCommodity.objects.all().order_by('commodity__mm_code').filter(is_active=True).filter(distribution_center=dc).exclude(id=commodity_id)
        return queryset

class CommoditiesCategoryOrder(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    serializer_class = DcCommodityForBatchSerializer
    filterset_fields = ['commodity__commodity_category__id', 'commodity__commodity_group__id']

    def get_queryset(self):
        dc_id = self.request.query_params.get('dcId')
        dc = DistributionCenter.objects.get(id=str(dc_id))
        queryset = DcCommodity.objects.all().filter(is_active=True).filter(distribution_center=dc)
        return queryset

class CommoditiesCategoryOrderSimilarProductsList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    # queryset = DcCommodity.objects.all().filter(is_active=True)
    serializer_class = DcCommodityForBatchSerializer
    filterset_fields = ['commodity__commodity_category__id', 'commodity__commodity_group__id']

    def get_queryset(self):
        dc_id = self.request.query_params.get('dcId')
        dc = DistributionCenter.objects.get(id=str(dc_id))
        commodity_id = self.request.query_params.get('comId')
        queryset = DcCommodity.objects.all().exclude(id=commodity_id).filter(is_active=True).filter(distribution_center=dc)
        return queryset

class CommoditiesDrugCodeSearch(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    serializer_class = DcCommodityForBatchSerializer
    search_fields = ['commodity__mm_code']

    def get_queryset(self):
        dc_id = self.request.query_params.get('dcId')
        dc = DistributionCenter.objects.get(id=str(dc_id))
        queryset = DcCommodity.objects.all().filter(is_active=True).filter(distribution_center=dc)
        return queryset

class CommoditiesGlobalSearch(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    # queryset = DcCommodity.objects.all().filter(available_quantity__gt=0)
    filter_backends = (SearchFilter,)
    serializer_class = DcCommodityForBatchSerializer
    search_fields = ['commodity__mm_code', 'commodity__name', 'commodity__commodity_category__name', 'commodity__commodity_group__name', 'commodity__salt_name']

    def get_queryset(self):
        letter = self.request.query_params.get('letter')
        dc_id = self.request.query_params.get('dcId')
        dc = DistributionCenter.objects.get(id=str(dc_id))
        queryset = DcCommodity.objects.all().filter(is_active=True).filter(distribution_center=dc)
        if letter:
            queryset = DcCommodity.objects.all().order_by('commodity__name').filter(Q(commodity__name__startswith=letter)|Q(commodity__name__startswith=letter.upper())).filter(is_active=True).filter(distribution_center=dc)
        return queryset
               