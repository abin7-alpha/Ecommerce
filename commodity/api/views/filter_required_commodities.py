from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from account.api.serializers.retailer_commodity_request import RetailerCommodityRequestSerializer
from account.models import Retailer, RetailerCommodityRequests

class RequestedRequiredCommodities(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    serializer_class = RetailerCommodityRequestSerializer
    filter_backends = (SearchFilter,)
    search_fields = ['dc_commodity__commodity__name', 'dc_commodity__commodity__mm_code']

    def get_queryset(self):
        retailer_id = self.request.query_params.get('retailerId')
        retailer_obj = Retailer.objects.get(id=retailer_id)
        try:
            availability = self.request.query_params.get('availability')
        except:
            availability = None
        queryset = None
        if availability:
            if availability == 'pending':
                queryset = RetailerCommodityRequests.objects.filter(retailer=retailer_obj).filter(is_active=True).all()
            elif availability == 'fulfilled':
                queryset = RetailerCommodityRequests.objects.filter(retailer=retailer_obj).filter(is_active=False).filter(is_deleted=False).all()
            elif availability == 'canceled':
                queryset = RetailerCommodityRequests.objects.filter(retailer=retailer_obj).filter(is_deleted=True).all()
        else:
            queryset = RetailerCommodityRequests.objects.filter(retailer=retailer_obj).all()
        return queryset
