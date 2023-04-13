from django.urls import path

# from commodity.api.views.get_com_by_region import get_commodities_by_region, get_com
from commodity.api.views.add_com_data import add_data_com
from commodity.api.views.filter_commodities import CommoditiesAlphabeticalOrderList, CommoditiesDrugCodeOrder
from commodity.api.views.filter_commodities import CommoditiesDrugCodeSearch, CommoditiesCategoryOrder
from commodity.api.views.filter_commodities import CommoditiesAlphabeticalOrderSimilarProductsList
from commodity.api.views.filter_commodities import CommoditiesDrugCodeOrderSimilarProductsList
from commodity.api.views.filter_commodities import CommoditiesCategoryOrderSimilarProductsList, CommoditiesAlphabeticalOrderAllList
from commodity.api.views.get_commodity_details_with_batch import get_commodity_details_with_batch
from commodity.api.views.request_commodity import request_commodity
from commodity.api.views.filter_required_commodities import RequestedRequiredCommodities
from commodity.api.views.mark_required_commodity import mark_commodity_not_required
from commodity.api.views.get_commodity_category_and_group import get_commodity_group_and_category
from commodity.api.views.get_commodity_details import get_commodity_details
from commodity.api.views.filter_commodities import CommoditiesGlobalSearch
from commodity.api.views.get_all_commodity_bathes import GetAllCommoditiesByDc, get_all_commodities_by_dc, search_commodities

from commodity.api.views.admin.get_all_commodities import get_all_commodities, get_all_inactive_commodities
from commodity.api.views.admin.get_all_dc_commodities import get_all_dc_commodities, get_all_inactive_dc_commodities
from commodity.api.views.admin.add_new_commodity import add_new_commodity
from commodity.api.views.admin.update_commodity import update_commodity
from commodity.api.views.admin.get_commodity_batch_details import get_batch_details
from commodity.api.views.admin.update_commodity_batch import update_commodity_batch
from commodity.api.views.admin.create_dc_commodity import create_dc_commodity
from commodity.api.views.admin.add_commodity_batch import add_commodity_batch
from commodity.api.views.admin.update_batch_available_quantity import update_commodity_batch_available_quantity
from commodity.api.views.admin.activate_or_deactivate_commodity import activate_or_deactivate_commodity
from commodity.api.views.admin.update_dc_commodity import update_dc_commodity
from commodity.api.views.admin.activate_or_deactivate_dc_commodity import activate_or_deactivate_dc_commodity
from commodity.api.views.check_commodity_availabilty_primary_dc import check_commodity_availability_primary_dc
from commodity.api.views.admin.get_all_commodities_low_stock_order import get_all_low_stock_commodities
from commodity.api.views.admin.get_all_dc_commodities import get_all_dc_commodities_non_janaushadi, get_all_inactive_dc_commodities_non_janaushadi
from commodity.api.views.admin.get_all_dc_commodities import search_dc_commodities, search_in_active_dc_commodities, search_dc_commodities_non_janaushadi, search_inactive_dc_commodities_non_janaushadi
from commodity.api.views.admin.get_all_commodities import search_all_commodities, search_inactive_commodities

urlpatterns = [
    # path('get-commodities-by-region', get_commodities_by_region, name='get_commodities_by_region'),
    # path('get-com', get_com, name='getcom'),
    path('add-com-data', add_data_com, name='add_com_data'),
    path('a-z-commodities', CommoditiesAlphabeticalOrderList.as_view(), name='commodities_by_alphabetical_order'),
    path('a-z-similiar-commodities', CommoditiesAlphabeticalOrderSimilarProductsList.as_view(), name='commodities_by_alphabetical_order_similiar_products_list'),
    path('commodities-by-drugcode', CommoditiesDrugCodeOrder.as_view(), name="commodities_by_drug_code"),
    path('commodities-by-drugcode-similar-commodities', CommoditiesDrugCodeOrderSimilarProductsList.as_view(), name="commodities_by_drug_code_similar_commodities"),
    path('commodities-by-category', CommoditiesCategoryOrder.as_view(), name="commodities_by_category_order"),
    path('commodities-by-category-similar-commodities', CommoditiesCategoryOrderSimilarProductsList.as_view(), name="commodities_by_category_order_similar_commodities"),
    path('commodities-global-search', CommoditiesGlobalSearch.as_view(), name="commodities_global_search"),
    path('search-commodities-drug-code', CommoditiesDrugCodeSearch.as_view(), name='search_commodities_by_drugcode'),
    path('get-commodity-details', get_commodity_details, name='get_commodity_details'),
    path('get-commodity-details-with-batches', get_commodity_details_with_batch, name='get_commodity_details_with_batch'),
    path('request-commodity', request_commodity, name='request_commodity'),
    path('required-commodities', RequestedRequiredCommodities.as_view(), name='requested_required_commodities'),
    path('get-commodity-category-and-group', get_commodity_group_and_category, name='get_commodity_group_and_category'),
    path('mark-distribution-store-indent-commodity', mark_commodity_not_required, name='mark_commodity_not_required'),
    path('commodities-by-alphabetical-order', CommoditiesAlphabeticalOrderAllList.as_view(), name='commodities_by_alphabetical_order'),
    path('check-commodity-availabilty-primary-dc', check_commodity_availability_primary_dc, name='check_commodity_availability_primary_dc'),
    path('get-all-commodities-by-dc', GetAllCommoditiesByDc.as_view(), name='get_all_commodities_by_dc'),
    path('get-all-order-commodities', get_all_commodities_by_dc, name='get_all_order_commodities'),
    path('search-commodities-for-order', search_commodities, name='search_commodities_for_order'),

    path('get-all-commodities', get_all_commodities, name='get_all_commodities'),
    path('search-all-commodities', search_all_commodities, name='search_all_commodities'),
    path('search-all-inactive-commodities', search_inactive_commodities, name='search_inactive_all_commodities'),
    path('search-dc-commodity', search_dc_commodities, name='search_dc_commodity'),
    path('search-dc-commodity-non-janaushadi', search_dc_commodities_non_janaushadi, name='search_dc_commodity_non_janaushadi'),
    path('search-inactive-dc-commodity', search_in_active_dc_commodities, name='search_inactive_dc_commodity'),
    path('search-inactive-dc-commodity-non-janaushadi', search_inactive_dc_commodities_non_janaushadi, name='search_inactive_dc_commodity_non_janaushadi'),
    path('get-all-inactive-commodities', get_all_inactive_commodities, name='get_all_inactive_commodities'),
    path('get-all-dc-commodities', get_all_dc_commodities, name='get_all_dc_commodities'),
    path('get-all-dc-commodities-non-janaushadi', get_all_dc_commodities_non_janaushadi, name='get_all_dc_commodities_non_janaushadi'),
    path('get-all-inactive-dc-commodities', get_all_inactive_dc_commodities, name='get_all_inactive_dc_commodities'),
    path('get-all-inactive-dc-commodities-non-janaushadi', get_all_inactive_dc_commodities_non_janaushadi, name='get_all_inactive_dc_commodities_non_janaushadi'),
    path('get-all-low-stock-commodities', get_all_low_stock_commodities, name='get_all_low_stock_commodities'),
    path('add-new-commodity', add_new_commodity, name='add_new_commodity'),
    path('update-commodity', update_commodity, name='update_commodity'),
    path('update-dc-commodity', update_dc_commodity, name='update_dc_commodity'),
    path('create-dc-commodity', create_dc_commodity, name='create_dc_commodity'),
    path('activate-or-deactivate-commodity', activate_or_deactivate_commodity, name='activate_or_deactivate_commodity'),
    path('get-batch-details', get_batch_details, name="get_batch_details"),
    path('update-commodity-batch', update_commodity_batch, name="update_commodity_batch"),
    path('add-commodity-batch', add_commodity_batch, name="add_commodity_batch"),
    path('update-commodity-batch-available-quantity', update_commodity_batch_available_quantity, name='update_commodity_batch_available_quantity'),
    path('activate-or-deactivate-dcCommodity', activate_or_deactivate_dc_commodity, name='activate_or_deactivate_dc_commodity')
]