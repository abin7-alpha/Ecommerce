from django.urls import path

from order.api.views.retailer_order import confirm_retailer_order
from order.api.views.get_order_details import get_order_details
from order.api.views.filter_order import GetRetailerOrders, GetRetailerOrdersByStatus
from order.api.views.get_all_orders import get_all_verified_orders, get_all_pending_orders, get_all_kerala_to_primary_orders
from order.api.views.get_all_orders import search_all_orders_verified, search_all_orders_pending, search_all_orders_in_packing, search_all_orders_packed, search_all_orders_kerala
from order.api.views.get_all_orders import search_all_orders_canceled, search_all_orders_delivered
from order.api.views.get_all_orders import get_all_packed_orders, get_all_in_packing_orders, get_all_canceled_orders, get_all_delivered_orders
from order.api.views.make_payment import make_payments_for_retailer
from order.api.views.retailer_order_commodity_from_primary_dc import confirm_retailer_order_commodities_from_primary_dc
from order.api.views.record_payment import record_payment_for_retailer
from order.api.views.retailer_address_for_ledger import get_ledger_data

from order.api.views.admin.get_all_payments import get_all_order_payments
from order.api.views.admin.get_retailer_payments import get_all_retailer_payments
from order.api.views.admin.verify_payment import verify_order_payment
from order.api.views.admin.confirm_retailer_order_by_admin import confirm_retailer_order_by_admin
from order.api.views.admin.mark_order_as_shipped import mark_order_as_shipped
from order.api.views.admin.mark_as_deliverd import mark_order_as_delivered
from order.api.views.admin.cancel_order_by_admin import cancel_order_admin
from order.api.views.ledger_api_credit import get_ledger_credit
from order.api.views.ledger_api_debit import get_ledger_debit
from order.api.views.admin.generate_otp_for_order_edit import generate_otp_for_retailer_order_edit_by_admin
from order.api.views.admin.edit_retailer_order_batch_quantity import retailer_order_batch_quantity_edit_by_admin
from order.api.views.admin.edit_retailer_order_batch_remove_by_admin import retailer_order_remove_batch_by_admin
from order.api.views.admin.approve_retailer_payment import approveRetailerPayment
from order.api.views.admin.ledger_credit_admin import get_ledger_credit_admin
from order.api.views.admin.importLedgerDataFromPdf import import_data_from_pdf
from order.api.views.admin.get_all_shipping_vendors import get_all_shipping_vendors
from order.api.views.admin.update_delivery_time import update_delivery_time
from order.api.views.admin.add_packing_time_start_end import add_packing_data_for_order
from order.api.views.admin.create_payments_towars_order import create_payment_for_order

urlpatterns = [
    path('confirm-retailer-order', confirm_retailer_order, name='confirm_retailer_order'),
    path('get-order-details', get_order_details, name='get_order_details'),
    path('search-all-orders-verified', search_all_orders_verified, name='search_all_orders_verified'),
    path('search-all-orders-pending', search_all_orders_pending, name='search_all_orders_pending'),
    path('search-all-orders-inpacking', search_all_orders_in_packing, name='search_all_orders_inpacking'),
    path('search-all-orders-packed', search_all_orders_packed, name='search_all_orders_packed'),
    path('search-all-orders-primary-dc', search_all_orders_kerala, name='search_all_orders_kerala'),
    path('search-all-orders-delivered', search_all_orders_delivered, name='search_all_orders_delivered'),
    path('search-all-orders-canceled', search_all_orders_canceled, name='search_all_orders_canceled'),
    path('get-all-orders-verified', get_all_verified_orders, name='get_all_orders_verified'),
    path('get-all-orders-pending', get_all_pending_orders, name='get_all_orders_pending'),
    path('get-all-orders-packed', get_all_packed_orders, name='get_all_orders_packed'),
    path('get-all-in-packing-orders', get_all_in_packing_orders, name='get_all_in_packing_orders'),
    path('get-all-orders-delivered', get_all_delivered_orders, name='get_all_orders_delivered'),
    path('get-all-orders-canceled', get_all_canceled_orders, name='get_all_orders_canceled'),
    path('get-all-orders-kerala-to-primary', get_all_kerala_to_primary_orders, name='get_all_orders_kerala_to_primary'),
    path('get-ledger-data', get_ledger_data, name='get_ledger_data'),
    path('get-retailer-orders', GetRetailerOrders.as_view(), name='get_retailer_orders'),
    path('get-retailer-orders-by-status', GetRetailerOrdersByStatus.as_view(), name='get_retailer_orders'),
    path('make-payments-for-retailer', make_payments_for_retailer, name='make_payments_for_retailer'),
    path('record-payment-for-retailer', record_payment_for_retailer, name='record_payment_for_retailer'),
    path('confirm-retailer-order-commodities-from-primary-dc', confirm_retailer_order_commodities_from_primary_dc, name='confirm_retailer_order_commodities_from_primary_dc'),
                                                                            
    path('get-all-order-payments', get_all_order_payments, name='get_all_order_payments'),
    path('approve-retailer-payments', approveRetailerPayment, name='approve_retailer_payments'),
    path('get-all-retailer-payments', get_all_retailer_payments, name='get_all_retailer_payments'),
    path('verify-order-payment', verify_order_payment, name='verify_order_payment'),
    path('confirm-retailer-order-by-admin', confirm_retailer_order_by_admin, name='confirm_retailer_order_by_admin'),
    path('mark-as-shipped', mark_order_as_shipped, name='mark_order_as_shipped'),
    path('mark-order-as-delivered', mark_order_as_delivered, name='mark_order_as_delivered'),
    path('cancel-order-by-admin', cancel_order_admin, name='cancel_order_admin'),
    path('get-ledger-credit', get_ledger_credit, name='get_ledger_credit'),
    path('get-ledger-credit-admin', get_ledger_credit_admin, name='get_ledger_credit_admin'),
    path('get-ledger-debit', get_ledger_debit, name='get_ledger_debit'),
    path('get-all-shipping-vendors', get_all_shipping_vendors, name='get_all_shipping_vendors'),
    path('generate-otp-for-retailer-order-edit-by-admin', generate_otp_for_retailer_order_edit_by_admin, name='generate_otp_for_retailer_order_edit_by_admin'),
    path('retailer-order-batch-quantity-edit-by-admin', retailer_order_batch_quantity_edit_by_admin, name='retailer_order_batch_quantity_edit_by_admin'),
    path('retailer-order-remove-batch-by-admin', retailer_order_remove_batch_by_admin, name='retailer_order_remove_batch_by_admin'),
    path('import-data-from-pdf', import_data_from_pdf, name='import_data_from_pdf'),
    path('update-delivery-time', update_delivery_time, name='update_delivery_time'),
    path('add-packing-data-for-order', add_packing_data_for_order, name='add_packing_data'),
    path('create-payment-for-order', create_payment_for_order, name='create_payment_for_order'),
]
