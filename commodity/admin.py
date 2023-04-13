from django.contrib import admin
from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import CommodityCategory, CommodityGroup, Commodity, DrugManufacturer
from .models import DcCommodity, DcCommodityBatch, DcCommodityBatchLog, DistributionStoreIndent
from .models import DistributionStoreIndentHistory, CommodityMeasuringUnits

class CommodityCategoryAdmin(admin.ModelAdmin):
	list_display=('id','name','is_active')
	search_fields=['id','name']

	# def distribution_center(self, instance):
	# 	return instance.user.name

class CommodityAdmin(admin.ModelAdmin):
	list_display=('id','name','is_active','updated', 'salt_name')
	search_fields=['id','name', 'salt_name']

	
class DcCommodityAdmin(admin.ModelAdmin):
	list_display=('id', 'commodity')
	search_fields=['id', 'commodity']

	def commodity(self, instance):
		return instance.commodity.name

	
class DcCommodityBatchAdmin(admin.ModelAdmin):
	list_display=('id', 'commodity_id', 'dc_commodity', 'price', 'updated', 'minimum_order_quantity', 'available_quantity')
	search_fields=['id', 'price', 'dc_commodity__id']

	def commodity_id(self, instance):
		return instance.dc_commodity.id

admin.site.register(CommodityCategory,CommodityCategoryAdmin)
admin.site.register(Commodity,CommodityAdmin)
admin.site.register(DcCommodity, DcCommodityAdmin)
admin.site.register(DcCommodityBatch, DcCommodityBatchAdmin)
admin.site.register(DcCommodityBatchLog)
admin.site.register(DistributionStoreIndent)
admin.site.register(DistributionStoreIndentHistory)
admin.site.register(CommodityGroup)
admin.site.register(DrugManufacturer)
admin.site.register(CommodityMeasuringUnits)
