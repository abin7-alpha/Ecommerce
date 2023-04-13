from django.contrib import admin
from .models import City, DistributionCenter, Area, NotificationRecords, DcDailyTransactions

class DistrbutionCenterAdmin(admin.ModelAdmin):
	list_display=('id','name','city','is_active')
	search_fields=['id','name','city']

class AreaAdmin(admin.ModelAdmin):
	list_display=('id','name','city','pincode')
	search_fields=['id','name']

class CityAdmin(admin.ModelAdmin):
	list_display=('id','name')
	search_fields=['id','name']

class DcDailyTransactionsAdmin(admin.ModelAdmin):
	list_display=('id','distribution_center','total_revenue','total_num_orders','date')
	search_fields=['id','distribution_center','date','total_num_orders']

	def dc_name(self, instance):
		if (instance.distribution_center):
			return instance.distribution_center.name 
		return ""

admin.site.register(DistributionCenter,DistrbutionCenterAdmin)
admin.site.register(Area,AreaAdmin)
admin.site.register(City,CityAdmin)
admin.site.register(NotificationRecords)
admin.site.register(DcDailyTransactions,DcDailyTransactionsAdmin)
