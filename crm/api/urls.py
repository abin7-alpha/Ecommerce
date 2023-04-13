from django.urls import path

from crm.api.views.create_service_request_guest import create_service_request_guest
from crm.api.views.create_service_request_retailer import create_service_request_retailer
from crm.api.views.get_service_requests import get_service_requests_retailer
from crm.api.views.create_query_message import create_message_query

from crm.api.views.admin.get_service_requests_admin import get_all_service_requests_admin
from crm.api.views.admin.reply_to_queries import reply_service_requests
from crm.api.views.admin.extract_data_pdf import extract_data_from_pdf

urlpatterns = [
    path('create-service-request-guest', create_service_request_guest, name='create_service_request_guest'),
    path('create-service-request-retailer', create_service_request_retailer, name='create_service_request_retailer'),
    path('get-service-requests', get_service_requests_retailer, name='get_service_requests_retailer'),
    path('create-query-message', create_message_query, name='create_query_message'),

    path('get-service-requests-admin', get_all_service_requests_admin, name='get_service_requests_admin'),
    path('reply_to_service_requests', reply_service_requests, name='reply_to_service_requests'),
    path('extract-data-from-pdf', extract_data_from_pdf, name='extract_data_from_pdf'),
]
