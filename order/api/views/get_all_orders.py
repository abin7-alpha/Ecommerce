import traceback, sys

from pytz import timezone
from datetime import datetime, timedelta

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status as Status
from rest_framework.response import Response

from django.core.paginator import Paginator
from django.db.models import Q

from order.models import Order, Retailer
from order.api.serializers.order import OrderSerializerForDetails

from account.decorators import is_order_manager
from account.models import Staff

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@is_order_manager()
def get_all_verified_orders(request):
    output = {}
    dc_id = request.query_params.get('dcId')
    page_number = request.query_params.get('pageNumber')
    staffId = request.query_params.get('userid')
    staff = Staff.objects.get(id=staffId)

    try:
        for dc in staff.dcs.all():
            if int(dc_id) == int(dc.id):
                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer__dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(~Q(status='Packed')).filter(~Q(status='Packing_Started')).order_by('-created')
                
                p = Paginator(all_orders, 20)
                current_page = p.page(int(page_number))

                all_orders_serializer = OrderSerializerForDetails(current_page.object_list, many=True)

                output['status'] = 'success'
                output['status_text'] = 'successfully fetched all the orders'
                output['total_pages'] = p.num_pages
                output['current_page_number'] = current_page.number
                output['previous'] = current_page.has_previous()
                output['next'] = current_page.has_next()
                output['count'] = p.count
                output['results'] = all_orders_serializer.data
                status = Status.HTTP_200_OK
            else:
                output['results'] = []
                status = Status.HTTP_200_OK
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'failed to fetch the orders'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@is_order_manager()
def search_all_orders_verified(request):
    output = {}
    data = request.data
    dc_id = data['dcId']
    page_number = data['pageNumber']
    staffId = request.data['userid']
    staff = Staff.objects.get(id=staffId)
    current_time = timezone('Asia/Kolkata').localize(datetime.now())

    try:
        retailer_key = data['retailer']
        search_key = data['searchKey']
        try:
            start_date_param = data['startDate']
            start_date_split = start_date_param.split('T')[0]
            start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
        except:
            start_date_param = current_time
            start_date = start_date_param + timedelta(days=1)
        end_date_param = data['endDate']
        end_date_split = end_date_param.split('T')[0]
        end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
        try:
            retailer = Retailer.objects.get(id=int(retailer_key))
            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(~Q(status='Packed')).filter(~Q(status='Packing_Started')).order_by('-created')
        except:
            retailer = Retailer.objects.get(user__name=retailer_key)
            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(~Q(status='Packed')).filter(~Q(status='Packing_Started')).order_by('-created')
    except:
        try:
            retailer_key = data['retailer']
            search_key = data['searchKey']
            try:
                retailer = Retailer.objects.get(id=int(retailer_key))
                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(~Q(status='Packed')).filter(~Q(status='Packing_Started')).filter(retailer=retailer).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
            except:
                retailer = Retailer.objects.get(user__name=retailer_key)
                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(~Q(status='Packed')).filter(~Q(status='Packing_Started')).filter(retailer=retailer).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
        except:
            try:
                retailer_key = data['retailer']
                try:
                    start_date_param = data['startDate']
                    start_date_split = start_date_param.split('T')[0]
                    start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
                except:
                    start_date_param = current_time
                    start_date = start_date_param + timedelta(days=1)
                end_date_param = data['endDate']
                end_date_split = end_date_param.split('T')[0]
                end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
                try:
                    retailer = Retailer.objects.get(id=int(retailer_key))
                    all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(~Q(status='Packed')).filter(~Q(status='Packing_Started')).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(retailer__dc__id=dc_id).order_by('-created')
                except:
                    retailer = Retailer.objects.get(user__name=retailer_key)
                    all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(~Q(status='Packed')).filter(~Q(status='Packing_Started')).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(retailer__dc__id=dc_id).order_by('-created')
            except:
                try:
                    search_key = data['searchKey']
                    try:
                        start_date_param = data['startDate']
                        start_date_split = start_date_param.split('T')[0]
                        start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
                    except:
                        start_date_param = current_time
                        start_date = start_date_param + timedelta(days=1)
                    end_date_param = data['endDate']
                    end_date_split = end_date_param.split('T')[0]
                    end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
                    all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(~Q(status='Packed')).filter(~Q(status='Packing_Started')).filter(created__range=(end_date, start_date)).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
                except:
                    try:
                        retailer_key = data['retailer']
                        try:
                            retailer = Retailer.objects.get(id=int(retailer_key))
                            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(~Q(status='Packed')).filter(~Q(status='Packing_Started')).filter(retailer=retailer).filter(retailer__dc__id=dc_id).order_by('-created')
                        except:
                            retailer = Retailer.objects.get(user__name=retailer_key)
                            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(~Q(status='Packed')).filter(~Q(status='Packing_Started')).filter(retailer=retailer).filter(retailer__dc__id=dc_id).order_by('-created')
                    except:
                        try:
                            search_key = data['searchKey']
                            try:
                                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(~Q(status='Packed')).filter(~Q(status='Packing_Started')).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
                            except:
                                raise Exception
                        except:
                            try:
                                try:
                                    start_date_param = data['startDate']
                                    start_date_split = start_date_param.split('T')[0]
                                    start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
                                except:
                                    start_date_param = current_time
                                    start_date = start_date_param + timedelta(days=1)
                                end_date_param = data['endDate']
                                end_date_split = end_date_param.split('T')[0]
                                end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
                                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(~Q(status='Packed')).filter(~Q(status='Packing_Started')).filter(created__range=(end_date, start_date)).filter(retailer__dc__id=dc_id).order_by('-created')
                            except:
                                raise Exception
    try:
    
        p = Paginator(all_orders, 200)
        current_page = p.page(int(page_number))

        all_orders_serializer = OrderSerializerForDetails(current_page.object_list, many=True)

        for dc in staff.dcs.all():
            if int(dc_id) == int(dc.id):
                output['status'] = 'success'
                output['status_text'] = 'successfully fetched all the orders'
                output['total_pages'] = p.num_pages
                output['current_page_number'] = current_page.number
                output['previous'] = current_page.has_previous()
                output['next'] = current_page.has_next()
                output['count'] = p.count
                output['results'] = all_orders_serializer.data
                status = Status.HTTP_200_OK
            else:
                output['results'] = []
                status = Status.HTTP_200_OK
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'failed to fetch the orders'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@is_order_manager()
def get_all_pending_orders(request):
    output = {}
    dc_id = request.query_params.get('dcId')
    page_number = request.query_params.get('pageNumber')
    staffId = request.query_params.get('userid')
    staff = Staff.objects.get(id=staffId)

    try:
        for dc in staff.dcs.all():
            if int(dc_id) == int(dc.id):
                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer__dc__id=dc_id).filter(is_admin_verified=False).filter(~Q(status='Cancelled')).order_by('-created')
                
                p = Paginator(all_orders, 20)
                current_page = p.page(int(page_number))

                all_orders_serializer = OrderSerializerForDetails(current_page.object_list, many=True)

                output['status'] = 'success'
                output['status_text'] = 'successfully fetched all the orders'
                output['total_pages'] = p.num_pages
                output['current_page_number'] = current_page.number
                output['previous'] = current_page.has_previous()
                output['next'] = current_page.has_next()
                output['count'] = p.count
                output['results'] = all_orders_serializer.data
                status = Status.HTTP_200_OK
            else:
                output['results'] = []
                status = Status.HTTP_200_OK
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'failed to fetch the orders'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@is_order_manager()
def search_all_orders_pending(request):
    output = {}
    data = request.data
    dc_id = data['dcId']
    page_number = data['pageNumber']
    current_time = timezone('Asia/Kolkata').localize(datetime.now())
    staffId = request.data['userid']
    staff = Staff.objects.get(id=staffId)

    try:
        retailer_key = data['retailer']
        search_key = data['searchKey']
        try:
            start_date_param = data['startDate']
            start_date_split = start_date_param.split('T')[0]
            start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
        except:
            start_date_param = current_time
            start_date = start_date_param + timedelta(days=1)
        end_date_param = data['endDate']
        end_date_split = end_date_param.split('T')[0]
        end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
        try:
            retailer = Retailer.objects.get(id=int(retailer_key))
            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).filter(is_admin_verified=False).filter(~Q(status='Cancelled')).order_by('-created')
        except:
            retailer = Retailer.objects.get(user__name=retailer_key)
            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).filter(is_admin_verified=False).filter(~Q(status='Cancelled')).order_by('-created')
    except:
        try:
            retailer_key = data['retailer']
            search_key = data['searchKey']
            try:
                retailer = Retailer.objects.get(id=int(retailer_key))
                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=False).filter(~Q(status='Cancelled')).filter(retailer=retailer).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
            except:
                retailer = Retailer.objects.get(user__name=retailer_key)
                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=False).filter(~Q(status='Cancelled')).filter(retailer=retailer).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
        except:
            try:
                retailer_key = data['retailer']
                try:
                    start_date_param = data['startDate']
                    start_date_split = start_date_param.split('T')[0]
                    start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
                except:
                    start_date_param = current_time
                    start_date = start_date_param + timedelta(days=1)
                end_date_param = data['endDate']
                end_date_split = end_date_param.split('T')[0]
                end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
                try:
                    retailer = Retailer.objects.get(id=int(retailer_key))
                    all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=False).filter(~Q(status='Cancelled')).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(retailer__dc__id=dc_id).order_by('-created')
                except:
                    retailer = Retailer.objects.get(user__name=retailer_key)
                    all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=False).filter(~Q(status='Cancelled')).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(retailer__dc__id=dc_id).order_by('-created')
            except:
                try:
                    search_key = data['searchKey']
                    try:
                        start_date_param = data['startDate']
                        start_date_split = start_date_param.split('T')[0]
                        start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
                    except:
                        start_date_param = current_time
                        start_date = start_date_param + timedelta(days=1)
                    end_date_param = data['endDate']
                    end_date_split = end_date_param.split('T')[0]
                    end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
                    all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=False).filter(~Q(status='Cancelled')).filter(created__range=(end_date, start_date)).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
                except:
                    try:
                        retailer_key = data['retailer']
                        try:
                            retailer = Retailer.objects.get(id=int(retailer_key))
                            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=False).filter(~Q(status='Cancelled')).filter(retailer=retailer).filter(retailer__dc__id=dc_id).order_by('-created')
                        except:
                            print("hi")
                            retailer = Retailer.objects.get(user__name=retailer_key)
                            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=False).filter(~Q(status='Cancelled')).filter(retailer=retailer).filter(retailer__dc__id=dc_id).order_by('-created')
                    except:
                        try:
                            search_key = data['searchKey']
                            try:
                                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=False).filter(~Q(status='Cancelled')).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
                            except:
                                raise Exception
                        except:
                            try:
                                try:
                                    start_date_param = data['startDate']
                                    start_date_split = start_date_param.split('T')[0]
                                    start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
                                except:
                                    start_date_param = current_time
                                    start_date = start_date_param + timedelta(days=1)
                                end_date_param = data['endDate']
                                end_date_split = end_date_param.split('T')[0]
                                end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
                                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=False).filter(~Q(status='Cancelled')).filter(created__range=(end_date, start_date)).filter(retailer__dc__id=dc_id).order_by('-created')
                            except:
                                all_orders = []
    try:
    
        p = Paginator(all_orders, 200)
        current_page = p.page(int(page_number))

        all_orders_serializer = OrderSerializerForDetails(current_page.object_list, many=True)

        for dc in staff.dcs.all():
            if int(dc_id) == int(dc.id):
                output['status'] = 'success'
                output['status_text'] = 'successfully fetched all the orders'
                output['total_pages'] = p.num_pages
                output['current_page_number'] = current_page.number
                output['previous'] = current_page.has_previous()
                output['next'] = current_page.has_next()
                output['count'] = p.count
                output['results'] = all_orders_serializer.data
                status = Status.HTTP_200_OK
            else:
                output['results'] = []
                status = Status.HTTP_200_OK
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'failed to fetch the orders'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@is_order_manager()
def get_all_packed_orders(request):
    output = {}
    dc_id = request.query_params.get('dcId')
    page_number = request.query_params.get('pageNumber')
    staffId = request.query_params.get('userid')
    staff = Staff.objects.get(id=staffId)

    try:
        for dc in staff.dcs.all():
            if int(dc_id) == int(dc.id):
                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer__dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packing_Started')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).order_by('-created')
                
                p = Paginator(all_orders, 20)
                current_page = p.page(int(page_number))

                all_orders_serializer = OrderSerializerForDetails(current_page.object_list, many=True)

                output['status'] = 'success'
                output['status_text'] = 'successfully fetched all the orders'
                output['total_pages'] = p.num_pages
                output['current_page_number'] = current_page.number
                output['previous'] = current_page.has_previous()
                output['next'] = current_page.has_next()
                output['count'] = p.count
                output['results'] = all_orders_serializer.data
                status = Status.HTTP_200_OK
            else:
                output['results'] = []
                status = Status.HTTP_200_OK
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'failed to fetch the orders'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@is_order_manager()
def search_all_orders_packed(request):
    output = {}
    data = request.data
    dc_id = data['dcId']
    page_number = data['pageNumber']
    current_time = timezone('Asia/Kolkata').localize(datetime.now())
    staffId = request.data['userid']
    staff = Staff.objects.get(id=staffId)

    try:
        retailer_key = data['retailer']
        search_key = data['searchKey']
        try:
            start_date_param = data['startDate']
            start_date_split = start_date_param.split('T')[0]
            start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
        except:
            start_date_param = current_time
            start_date = start_date_param + timedelta(days=1)
        end_date_param = data['endDate']
        end_date_split = end_date_param.split('T')[0]
        end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
        try:
            retailer = Retailer.objects.get(id=int(retailer_key))
            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packing_Started')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).order_by('-created')
        except:
            retailer = Retailer.objects.get(user__name=retailer_key)
            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packing_Started')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).order_by('-created')
    except:
        try:
            retailer_key = data['retailer']
            search_key = data['searchKey']
            try:
                retailer = Retailer.objects.get(id=int(retailer_key))
                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packing_Started')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(retailer=retailer).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
            except:
                retailer = Retailer.objects.get(user__name=retailer_key)
                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packing_Started')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(retailer=retailer).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
        except:
            try:
                retailer_key = data['retailer']
                try:
                    start_date_param = data['startDate']
                    start_date_split = start_date_param.split('T')[0]
                    start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
                except:
                    start_date_param = current_time
                    start_date = start_date_param + timedelta(days=1)
                end_date_param = data['endDate']
                end_date_split = end_date_param.split('T')[0]
                end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
                try:
                    retailer = Retailer.objects.get(id=int(retailer_key))
                    all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packing_Started')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(retailer__dc__id=dc_id).order_by('-created')
                except:
                    retailer = Retailer.objects.get(user__name=retailer_key)
                    all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packing_Started')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(retailer__dc__id=dc_id).order_by('-created')
            except:
                try:
                    search_key = data['searchKey']
                    try:
                        start_date_param = data['startDate']
                        start_date_split = start_date_param.split('T')[0]
                        start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
                    except:
                        start_date_param = current_time
                        start_date = start_date_param + timedelta(days=1)
                    end_date_param = data['endDate']
                    end_date_split = end_date_param.split('T')[0]
                    end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
                    all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packing_Started')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(created__range=(end_date, start_date)).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
                except:
                    try:
                        retailer_key = data['retailer']
                        try:
                            retailer = Retailer.objects.get(id=int(retailer_key))
                            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packing_Started')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(retailer=retailer).filter(retailer__dc__id=dc_id).order_by('-created')
                        except:
                            retailer = Retailer.objects.get(user__name=retailer_key)
                            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packing_Started')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(retailer=retailer).filter(retailer__dc__id=dc_id).order_by('-created')
                    except:
                        try:
                            search_key = data['searchKey']
                            try:
                                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packing_Started')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
                            except:
                                raise Exception
                        except:
                            try:
                                try:
                                    start_date_param = data['startDate']
                                    start_date_split = start_date_param.split('T')[0]
                                    start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
                                except:
                                    start_date_param = current_time
                                    start_date = start_date_param + timedelta(days=1)
                                end_date_param = data['endDate']
                                end_date_split = end_date_param.split('T')[0]
                                end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
                                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packing_Started')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(created__range=(end_date, start_date)).filter(retailer__dc__id=dc_id).order_by('-created')
                            except:
                                raise Exception
    try:
    
        p = Paginator(all_orders, 200)
        current_page = p.page(int(page_number))

        all_orders_serializer = OrderSerializerForDetails(current_page.object_list, many=True)

        for dc in staff.dcs.all():
            if int(dc_id) == int(dc.id):
                output['status'] = 'success'
                output['status_text'] = 'successfully fetched all the orders'
                output['total_pages'] = p.num_pages
                output['current_page_number'] = current_page.number
                output['previous'] = current_page.has_previous()
                output['next'] = current_page.has_next()
                output['count'] = p.count
                output['results'] = all_orders_serializer.data
                status = Status.HTTP_200_OK
            else:
                output['results'] = []
                status = Status.HTTP_200_OK
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'failed to fetch the orders'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@is_order_manager()
def get_all_in_packing_orders(request):
    output = {}
    dc_id = request.query_params.get('dcId')
    page_number = request.query_params.get('pageNumber')
    staffId = request.query_params.get('userid')
    staff = Staff.objects.get(id=staffId)

    try:
        for dc in staff.dcs.all():
            if int(dc_id) == int(dc.id):
                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer__dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).order_by('-created')
                
                p = Paginator(all_orders, 20)
                current_page = p.page(int(page_number))

                all_orders_serializer = OrderSerializerForDetails(current_page.object_list, many=True)

                output['status'] = 'success'
                output['status_text'] = 'successfully fetched all the orders'
                output['total_pages'] = p.num_pages
                output['current_page_number'] = current_page.number
                output['previous'] = current_page.has_previous()
                output['next'] = current_page.has_next()
                output['count'] = p.count
                output['results'] = all_orders_serializer.data
                status = Status.HTTP_200_OK
            else:
                output['results'] = []
                status = Status.HTTP_200_OK
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'failed to fetch the orders'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@is_order_manager()
def search_all_orders_in_packing(request):
    output = {}
    data = request.data
    dc_id = data['dcId']
    page_number = data['pageNumber']
    current_time = timezone('Asia/Kolkata').localize(datetime.now())
    staffId = request.data['userid']
    staff = Staff.objects.get(id=staffId)

    try:
        retailer_key = data['retailer']
        search_key = data['searchKey']
        try:
            start_date_param = data['startDate']
            start_date_split = start_date_param.split('T')[0]
            start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
        except:
            start_date_param = current_time
            start_date = start_date_param + timedelta(days=1)
        end_date_param = data['endDate']
        end_date_split = end_date_param.split('T')[0]
        end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
        try:
            retailer = Retailer.objects.get(id=int(retailer_key))
            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).order_by('-created')
        except:
            retailer = Retailer.objects.get(user__name=retailer_key)
            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).order_by('-created')
    except:
        try:
            retailer_key = data['retailer']
            search_key = data['searchKey']
            try:
                retailer = Retailer.objects.get(id=int(retailer_key))
                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(retailer=retailer).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
            except:
                retailer = Retailer.objects.get(user__name=retailer_key)
                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(retailer=retailer).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
        except:
            try:
                retailer_key = data['retailer']
                try:
                    start_date_param = data['startDate']
                    start_date_split = start_date_param.split('T')[0]
                    start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
                except:
                    start_date_param = current_time
                    start_date = start_date_param + timedelta(days=1)
                end_date_param = data['endDate']
                end_date_split = end_date_param.split('T')[0]
                end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
                try:
                    retailer = Retailer.objects.get(id=int(retailer_key))
                    all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(retailer__dc__id=dc_id).order_by('-created')
                except:
                    retailer = Retailer.objects.get(user__name=retailer_key)
                    all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(retailer__dc__id=dc_id).order_by('-created')
            except:
                try:
                    search_key = data['searchKey']
                    try:
                        start_date_param = data['startDate']
                        start_date_split = start_date_param.split('T')[0]
                        start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
                    except:
                        start_date_param = current_time
                        start_date = start_date_param + timedelta(days=1)
                    end_date_param = data['endDate']
                    end_date_split = end_date_param.split('T')[0]
                    end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
                    all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(created__range=(end_date, start_date)).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
                except:
                    try:
                        retailer_key = data['retailer']
                        try:
                            retailer = Retailer.objects.get(id=int(retailer_key))
                            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(retailer=retailer).filter(retailer__dc__id=dc_id).order_by('-created')
                        except:
                            retailer = Retailer.objects.get(user__name=retailer_key)
                            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(retailer=retailer).filter(retailer__dc__id=dc_id).order_by('-created')
                    except:
                        try:
                            search_key = data['searchKey']
                            try:
                                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
                            except:
                                raise Exception
                        except:
                            try:
                                try:
                                    start_date_param = data['startDate']
                                    start_date_split = start_date_param.split('T')[0]
                                    start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
                                except:
                                    start_date_param = current_time
                                    start_date = start_date_param + timedelta(days=1)
                                end_date_param = data['endDate']
                                end_date_split = end_date_param.split('T')[0]
                                end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
                                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Delivered')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(created__range=(end_date, start_date)).filter(retailer__dc__id=dc_id).order_by('-created')
                            except:
                                raise Exception
    try:
    
        p = Paginator(all_orders, 200)
        current_page = p.page(int(page_number))

        all_orders_serializer = OrderSerializerForDetails(current_page.object_list, many=True)

        for dc in staff.dcs.all():
            if int(dc_id) == int(dc.id):
                output['status'] = 'success'
                output['status_text'] = 'successfully fetched all the orders'
                output['total_pages'] = p.num_pages
                output['current_page_number'] = current_page.number
                output['previous'] = current_page.has_previous()
                output['next'] = current_page.has_next()
                output['count'] = p.count
                output['results'] = all_orders_serializer.data
                status = Status.HTTP_200_OK
            else:
                output['results'] = []
                status = Status.HTTP_200_OK
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'failed to fetch the orders'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@is_order_manager()
def get_all_delivered_orders(request):
    output = {}
    dc_id = request.query_params.get('dcId')
    page_number = request.query_params.get('pageNumber')
    staffId = request.query_params.get('userid')
    staff = Staff.objects.get(id=staffId)

    try:
        for dc in staff.dcs.all():
            if int(dc_id) == int(dc.id):
                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer__dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).order_by('-created')
                
                p = Paginator(all_orders, 20)
                current_page = p.page(int(page_number))

                all_orders_serializer = OrderSerializerForDetails(current_page.object_list, many=True)

                output['status'] = 'success'
                output['status_text'] = 'successfully fetched all the orders'
                output['total_pages'] = p.num_pages
                output['current_page_number'] = current_page.number
                output['previous'] = current_page.has_previous()
                output['next'] = current_page.has_next()
                output['count'] = p.count
                output['results'] = all_orders_serializer.data
                status = Status.HTTP_200_OK
            else:
                output['results'] = []
                status = Status.HTTP_200_OK
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'failed to fetch the orders'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@is_order_manager()
def search_all_orders_delivered(request):
    output = {}
    data = request.data
    dc_id = data['dcId']
    page_number = data['pageNumber']
    current_time = timezone('Asia/Kolkata').localize(datetime.now())
    staffId = request.data['userid']
    staff = Staff.objects.get(id=staffId)

    try:
        retailer_key = data['retailer']
        search_key = data['searchKey']
        try:
            start_date_param = data['startDate']
            start_date_split = start_date_param.split('T')[0]
            start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
        except:
            start_date_param = current_time
            start_date = start_date_param + timedelta(days=1)
        end_date_param = data['endDate']
        end_date_split = end_date_param.split('T')[0]
        end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
        try:
            retailer = Retailer.objects.get(id=int(retailer_key))
            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).order_by('-created')
        except:
            retailer = Retailer.objects.get(user__name=retailer_key)
            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).order_by('-created')
    except:
        try:
            retailer_key = data['retailer']
            search_key = data['searchKey']
            try:
                retailer = Retailer.objects.get(id=int(retailer_key))
                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(retailer=retailer).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
            except:
                retailer = Retailer.objects.get(user__name=retailer_key)
                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(retailer=retailer).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
        except:
            try:
                retailer_key = data['retailer']
                try:
                    start_date_param = data['startDate']
                    start_date_split = start_date_param.split('T')[0]
                    start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
                except:
                    start_date_param = current_time
                    start_date = start_date_param + timedelta(days=1)
                end_date_param = data['endDate']
                end_date_split = end_date_param.split('T')[0]
                end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
                try:
                    retailer = Retailer.objects.get(id=int(retailer_key))
                    all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(retailer__dc__id=dc_id).order_by('-created')
                except:
                    retailer = Retailer.objects.get(user__name=retailer_key)
                    all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(retailer__dc__id=dc_id).order_by('-created')
            except:
                try:
                    search_key = data['searchKey']
                    try:
                        start_date_param = data['startDate']
                        start_date_split = start_date_param.split('T')[0]
                        start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
                    except:
                        start_date_param = current_time
                        start_date = start_date_param + timedelta(days=1)
                    end_date_param = data['endDate']
                    end_date_split = end_date_param.split('T')[0]
                    end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
                    all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(created__range=(end_date, start_date)).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
                except:
                    try:
                        retailer_key = data['retailer']
                        try:
                            retailer = Retailer.objects.get(id=int(retailer_key))
                            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(retailer=retailer).filter(retailer__dc__id=dc_id).order_by('-created')
                        except:
                            print("hi")
                            retailer = Retailer.objects.get(user__name=retailer_key)
                            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(retailer=retailer).filter(retailer__dc__id=dc_id).order_by('-created')
                    except:
                        try:
                            search_key = data['searchKey']
                            try:
                                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
                            except:
                                raise Exception
                        except:
                            try:
                                try:
                                    start_date_param = data['startDate']
                                    start_date_split = start_date_param.split('T')[0]
                                    start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
                                except:
                                    start_date_param = current_time
                                    start_date = start_date_param + timedelta(days=1)
                                end_date_param = data['endDate']
                                end_date_split = end_date_param.split('T')[0]
                                end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
                                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Cancelled')).filter(~Q(status='Delivery_In_Progress')).filter(created__range=(end_date, start_date)).filter(retailer__dc__id=dc_id).order_by('-created')
                            except:
                                all_orders = []
    try:
    
        p = Paginator(all_orders, 200)
        current_page = p.page(int(page_number))

        all_orders_serializer = OrderSerializerForDetails(current_page.object_list, many=True)

        for dc in staff.dcs.all():
            if int(dc_id) == int(dc.id):
                output['status'] = 'success'
                output['status_text'] = 'successfully fetched all the orders'
                output['total_pages'] = p.num_pages
                output['current_page_number'] = current_page.number
                output['previous'] = current_page.has_previous()
                output['next'] = current_page.has_next()
                output['count'] = p.count
                output['results'] = all_orders_serializer.data
                status = Status.HTTP_200_OK
            else:
                output['results'] = []
                status = Status.HTTP_200_OK
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'failed to fetch the orders'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@is_order_manager()
def get_all_canceled_orders(request):
    output = {}
    dc_id = request.query_params.get('dcId')
    page_number = request.query_params.get('pageNumber')
    staffId = request.query_params.get('userid')
    staff = Staff.objects.get(id=staffId)

    try:
        for dc in staff.dcs.all():
            if int(dc_id) == int(dc.id):
                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer__dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Delivered')).filter(~Q(status='Delivery_In_Progress')).order_by('-created')
                
                p = Paginator(all_orders, 20)
                current_page = p.page(int(page_number))

                all_orders_serializer = OrderSerializerForDetails(current_page.object_list, many=True)

                output['status'] = 'success'
                output['status_text'] = 'successfully fetched all the orders'
                output['total_pages'] = p.num_pages
                output['current_page_number'] = current_page.number
                output['previous'] = current_page.has_previous()
                output['next'] = current_page.has_next()
                output['count'] = p.count
                output['results'] = all_orders_serializer.data
                status = Status.HTTP_200_OK
            else:
                output['results'] = []
                status = Status.HTTP_200_OK
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'failed to fetch the orders'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@is_order_manager()
def search_all_orders_canceled(request):
    output = {}
    data = request.data
    dc_id = data['dcId']
    page_number = data['pageNumber']
    current_time = timezone('Asia/Kolkata').localize(datetime.now())
    staffId = request.data['userid']
    staff = Staff.objects.get(id=staffId)

    try:
        retailer_key = data['retailer']
        search_key = data['searchKey']
        try:
            start_date_param = data['startDate']
            start_date_split = start_date_param.split('T')[0]
            start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
        except:
            start_date_param = current_time
            start_date = start_date_param + timedelta(days=1)
        end_date_param = data['endDate']
        end_date_split = end_date_param.split('T')[0]
        end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
        try:
            retailer = Retailer.objects.get(id=int(retailer_key))
            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Delivered')).filter(~Q(status='Delivery_In_Progress')).order_by('-created')
        except:
            retailer = Retailer.objects.get(user__name=retailer_key)
            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Delivered')).filter(~Q(status='Delivery_In_Progress')).order_by('-created')
    except:
        try:
            retailer_key = data['retailer']
            search_key = data['searchKey']
            try:
                retailer = Retailer.objects.get(id=int(retailer_key))
                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Delivered')).filter(~Q(status='Delivery_In_Progress')).filter(retailer=retailer).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
            except:
                retailer = Retailer.objects.get(user__name=retailer_key)
                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Delivered')).filter(~Q(status='Delivery_In_Progress')).filter(retailer=retailer).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
        except:
            try:
                retailer_key = data['retailer']
                try:
                    start_date_param = data['startDate']
                    start_date_split = start_date_param.split('T')[0]
                    start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
                except:
                    start_date_param = current_time
                    start_date = start_date_param + timedelta(days=1)
                end_date_param = data['endDate']
                end_date_split = end_date_param.split('T')[0]
                end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
                try:
                    retailer = Retailer.objects.get(id=int(retailer_key))
                    all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Delivered')).filter(~Q(status='Delivery_In_Progress')).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(retailer__dc__id=dc_id).order_by('-created')
                except:
                    retailer = Retailer.objects.get(user__name=retailer_key)
                    all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Delivered')).filter(~Q(status='Delivery_In_Progress')).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(retailer__dc__id=dc_id).order_by('-created')
            except:
                try:
                    search_key = data['searchKey']
                    try:
                        start_date_param = data['startDate']
                        start_date_split = start_date_param.split('T')[0]
                        start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
                    except:
                        start_date_param = current_time
                        start_date = start_date_param + timedelta(days=1)
                    end_date_param = data['endDate']
                    end_date_split = end_date_param.split('T')[0]
                    end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
                    all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Delivered')).filter(~Q(status='Delivery_In_Progress')).filter(created__range=(end_date, start_date)).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
                except:
                    try:
                        retailer_key = data['retailer']
                        try:
                            retailer = Retailer.objects.get(id=int(retailer_key))
                            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Delivered')).filter(~Q(status='Delivery_In_Progress')).filter(retailer=retailer).filter(retailer__dc__id=dc_id).order_by('-created')
                        except:
                            print("hi")
                            retailer = Retailer.objects.get(user__name=retailer_key)
                            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Delivered')).filter(~Q(status='Delivery_In_Progress')).filter(retailer=retailer).filter(retailer__dc__id=dc_id).order_by('-created')
                    except:
                        try:
                            search_key = data['searchKey']
                            try:
                                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Delivered')).filter(~Q(status='Delivery_In_Progress')).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__id=dc_id).order_by('-created')
                            except:
                                raise Exception
                        except:
                            try:
                                try:
                                    start_date_param = data['startDate']
                                    start_date_split = start_date_param.split('T')[0]
                                    start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
                                except:
                                    start_date_param = current_time
                                    start_date = start_date_param + timedelta(days=1)
                                end_date_param = data['endDate']
                                end_date_split = end_date_param.split('T')[0]
                                end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
                                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(is_admin_verified=True).filter(~Q(status='Packing_Started')).filter(~Q(status='Packed')).filter(~Q(status='New')).filter(~Q(status='Delivered')).filter(~Q(status='Delivery_In_Progress')).filter(created__range=(end_date, start_date)).filter(retailer__dc__id=dc_id).order_by('-created')
                            except:
                                all_orders = []
    try:
    
        p = Paginator(all_orders, 200)
        current_page = p.page(int(page_number))

        all_orders_serializer = OrderSerializerForDetails(current_page.object_list, many=True)

        for dc in staff.dcs.all():
            if int(dc_id) == int(dc.id):
                output['status'] = 'success'
                output['status_text'] = 'successfully fetched all the orders'
                output['total_pages'] = p.num_pages
                output['current_page_number'] = current_page.number
                output['previous'] = current_page.has_previous()
                output['next'] = current_page.has_next()
                output['count'] = p.count
                output['results'] = all_orders_serializer.data
                status = Status.HTTP_200_OK
            else:
                output['results'] = []
                status = Status.HTTP_200_OK
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'failed to fetch the orders'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@is_order_manager()
def get_all_kerala_to_primary_orders(request):
    output = {}
    dc_id = request.query_params.get('dcId')
    page_number = request.query_params.get('pageNumber')
    staffId = request.query_params.get('userid')
    staff = Staff.objects.get(id=staffId)

    try:
        for dc in staff.dcs.all():
            if int(dc_id) == int(dc.id):
                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer__dc__is_primary_dC=False).order_by('-created')
                
                p = Paginator(all_orders, 20)
                current_page = p.page(int(page_number))

                all_orders_serializer = OrderSerializerForDetails(current_page.object_list, many=True)

                output['status'] = 'success'
                output['status_text'] = 'successfully fetched all the orders'
                output['total_pages'] = p.num_pages
                output['current_page_number'] = current_page.number
                output['previous'] = current_page.has_previous()
                output['next'] = current_page.has_next()
                output['count'] = p.count
                output['results'] = all_orders_serializer.data
                status = Status.HTTP_200_OK
            else:
                output['results'] = []
                status = Status.HTTP_200_OK
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'failed to fetch the orders'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@is_order_manager()
def search_all_orders_kerala(request):
    output = {}
    data = request.data
    dc_id = data['dcId']
    page_number = data['pageNumber']
    current_time = timezone('Asia/Kolkata').localize(datetime.now())
    staffId = request.data['userid']
    staff = Staff.objects.get(id=staffId)

    try:
        retailer_key = data['retailer']
        search_key = data['searchKey']
        try:
            start_date_param = data['startDate']
            start_date_split = start_date_param.split('T')[0]
            start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
        except:
            start_date_param = current_time
            start_date = start_date_param + timedelta(days=1)
        end_date_param = data['endDate']
        end_date_split = end_date_param.split('T')[0]
        end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
        try:
            retailer = Retailer.objects.get(id=int(retailer_key))
            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__is_primary_dC=False).order_by('-created')
        except:
            retailer = Retailer.objects.get(user__name=retailer_key)
            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer=retailer).filter(created__range=(end_date, start_date)).filter(Q(order_no=search_key) | Q(amount=search_key)).filter(retailer__dc__is_primary_dC=False).order_by('-created')
    except:
        try:
            retailer_key = data['retailer']
            search_key = data['searchKey']
            try:
                retailer = Retailer.objects.get(id=int(retailer_key))
                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer__dc__is_primary_dC=False).filter(retailer=retailer).filter(Q(order_no=search_key) | Q(amount=search_key)).order_by('-created')
            except:
                retailer = Retailer.objects.get(user__name=retailer_key)
                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer__dc__is_primary_dC=False).filter(retailer=retailer).filter(Q(order_no=search_key) | Q(amount=search_key)).order_by('-created')
        except:
            try:
                retailer_key = data['retailer']
                try:
                    start_date_param = data['startDate']
                    start_date_split = start_date_param.split('T')[0]
                    start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
                except:
                    start_date_param = current_time
                    start_date = start_date_param + timedelta(days=1)
                end_date_param = data['endDate']
                end_date_split = end_date_param.split('T')[0]
                end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
                try:
                    retailer = Retailer.objects.get(id=int(retailer_key))
                    all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer__dc__is_primary_dC=False).filter(retailer=retailer).filter(created__range=(end_date, start_date)).order_by('-created')
                except:
                    retailer = Retailer.objects.get(user__name=retailer_key)
                    all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer__dc__is_primary_dC=False).filter(retailer=retailer).filter(created__range=(end_date, start_date)).order_by('-created')
            except:
                try:
                    search_key = data['searchKey']
                    try:
                        start_date_param = data['startDate']
                        start_date_split = start_date_param.split('T')[0]
                        start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
                    except:
                        start_date_param = current_time
                        start_date = start_date_param + timedelta(days=1)
                    end_date_param = data['endDate']
                    end_date_split = end_date_param.split('T')[0]
                    end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
                    all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer__dc__is_primary_dC=False).filter(created__range=(end_date, start_date)).filter(Q(order_no=search_key) | Q(amount=search_key)).order_by('-created')
                except:
                    try:
                        retailer_key = data['retailer']
                        try:
                            retailer = Retailer.objects.get(id=int(retailer_key))
                            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer__dc__is_primary_dC=False).filter(retailer=retailer).order_by('-created')
                        except:
                            retailer = Retailer.objects.get(user__name=retailer_key)
                            all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer__dc__is_primary_dC=False).filter(retailer=retailer).order_by('-created')
                    except:
                        try:
                            search_key = data['searchKey']
                            try:
                                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer__dc__is_primary_dC=False).filter(Q(order_no=search_key) | Q(amount=search_key)).order_by('-created')
                            except:
                                raise Exception
                        except:
                            try:
                                try:
                                    start_date_param = data['startDate']
                                    start_date_split = start_date_param.split('T')[0]
                                    start_date = datetime.strptime(start_date_split, '%Y-%m-%d') + timedelta(days=1)
                                except:
                                    start_date_param = current_time
                                    start_date = start_date_param + timedelta(days=1)
                                end_date_param = data['endDate']
                                end_date_split = end_date_param.split('T')[0]
                                end_date = datetime.strptime(end_date_split, '%Y-%m-%d')
                                all_orders = Order.objects.filter(dispatch_dc__id=dc_id).filter(retailer__dc__is_primary_dC=False).filter(created__range=(end_date, start_date)).order_by('-created')
                            except:
                                raise Exception
    try:
    
        p = Paginator(all_orders, 200)
        current_page = p.page(int(page_number))

        all_orders_serializer = OrderSerializerForDetails(current_page.object_list, many=True)

        for dc in staff.dcs.all():
            if int(dc_id) == int(dc.id):
                output['status'] = 'success'
                output['status_text'] = 'successfully fetched all the orders'
                output['total_pages'] = p.num_pages
                output['current_page_number'] = current_page.number
                output['previous'] = current_page.has_previous()
                output['next'] = current_page.has_next()
                output['count'] = p.count
                output['results'] = all_orders_serializer.data
                status = Status.HTTP_200_OK
            else:
                output['results'] = []
                status = Status.HTTP_200_OK
    except:
        traceback.print_exc(file=sys.stdout)
        output['status'] = 'failed'
        output['status_text'] = 'failed to fetch the orders'
        status = Status.HTTP_400_BAD_REQUEST

    return Response(output, status=status)

