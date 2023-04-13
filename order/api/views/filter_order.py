from pytz import timezone
from datetime import datetime, timedelta

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from account.models import Retailer
from account.api.serializers.retailer_serializer import RetailerOrderSerializer

from order.models import Order
from order.api.serializers.order import OrderSerializer, OrderSerializerForDetails

class GetRetailerOrders(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    queryset = Order.objects.all()
    filter_backends = (SearchFilter,)
    serializer_class = OrderSerializer
    search_fields = ['order_no']

class GetRetailerOrdersByStatus(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    # filter_backends = [DjangoFilterBackend]
    # queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # filterset_fields = ['retailer__id', 'status']

    def get_queryset(self):
        status = self.request.query_params.get('status')
        start_date_param = str(self.request.query_params.get('startDate'))
        end_date_param = str(self.request.query_params.get('endDate'))
        start_date_split = datetime.strptime(start_date_param, "%m/%d/%Y")
        print(start_date_split)
        end_date_split = end_date_param.split('/')
        start_date = start_date_split + timedelta(days=1)
        end_date = f'{end_date_split[2]}-{end_date_split[0]}-{end_date_split[1]}'
        retailer_id = self.request.query_params.get('retailerId')
        retailer = Retailer.objects.get(id=retailer_id)
        # current_date = timezone('Asia/Kolkata').localize(datetime.now()) + timedelta(1)
        # formated_current_date = current_date.strftime("%Y-%m-%d")
        # formated_start_date = start_date.strftime("%Y-%m-%d")
        if status:
            queryset = Order.objects.filter(retailer=retailer).filter(status=status).filter(created__range=(end_date, start_date)).order_by('-created')
            return queryset
        else:
            queryset = Order.objects.filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(Q(amount__gt=0)).order_by('-created')
            return queryset
        # if status == 'pending':
        #     queryset = Order.objects.filter(retailer=retailer).filter(Q(amount__gt=0)).filter(created__range=(formated_start_date, formated_current_date))
        #     return queryset
        # if status == 'completed':
        #     queryset = Order.objects.filter(retailer=retailer).filter(Q(amount=0)).filter(created__range=(formated_start_date, formated_current_date))
        #     return queryset
        # else:
        #     queryset = Order.objects.filter(retailer=retailer).filter(created__range=(formated_start_date, formated_current_date))
        #     return queryset
        