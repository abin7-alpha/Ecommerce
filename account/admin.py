from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import BasicUser, AddressType, Addresses, Retailer, RetailerNotification
from .models import RetailerShop, DistributionCenterManager, Staff
from .models import RetailerDevice, City, Banks, DistributionManagerloggedInData
from .models import RetailerCommodityRequests, RetailerNotification, NotificationType, Device

# class HumusAdminSite(AdminSite):
# 	site_header = 'Humus Admin Interface'
# 	site_title = 'Humus Administration'
# 	index_title = 'Humus Administration'
# 	site_url = None

class BasicUserAdmin(admin.ModelAdmin):
	list_display=('id','name','email','phone','passcode','last_logged_in','is_active','is_email_verified')
	search_fields=['id','name','email','phone','passcode']

class AddressTypeAdmin(admin.ModelAdmin):
	list_display=('id','name','is_active')
	search_fields=['id','name']

class AddressAdmin(admin.ModelAdmin):
	list_display=('id','city','country','zipcode')
	search_fields=['id','zipcode']

class RetailerShopAdmin(admin.ModelAdmin):
	list_display=('id', 'shop_name')

class RetailerAdmin(admin.ModelAdmin):
	list_display=('id','retailer_name','retailer_phone','retailer_email','retailer_address')
	search_fields=['id','shopName','shopCode']

	def retailer_name(self, instance):
		return instance.user.name

	def retailer_phone(self, instance):
		return instance.user.phone

	def retailer_address(self, instance):
		if instance.address!=None:
			return instance.address.line1 +" :: "+instance.address.city+" :: "+instance.address.country
		else:
			return "None"
	
	def retailer_email(self, instance):
		return instance.user.email

class DMAdmin(admin.ModelAdmin):
	list_display=('id','manager_name','is_active')
	search_fields=['id','manager_name']

	def manager_name(self, instance):
		return instance.user.name

# class CustomerAdmin(admin.ModelAdmin):
# 	list_display=('id','name','phone','email','isActive','distributor')
# 	search_fields=['id','name','phone','email']

# 	def distributor(self, instance):
# 		if (instance.Distributor):
# 			return instance.Distributor.name 
# 		return ""


# class DistributorAdmin(admin.ModelAdmin):
# 	list_display=('id','name','phone','email','isActive','isDeliveryAvailable','distributor_area')
# 	search_fields=['id','name','phone','email','isDeliveryAvailable']

# 	def distributor_area(self, instance):
# 		area=""
# 		if (instance.areaOfOperation!=None):
# 			area=instance.areaOfOperation.name+" :: "+instance.areaOfOperation.city
# 		return area

class StaffAdmin(admin.ModelAdmin):
	list_display=('id','name','phone','passcode','dcs','is_active','is_logistics_manager',
				  'is_order_manager','is_payments_manager','is_super_admin', 'is_retailer_manager')
	search_fields=['id']

	# def staff_name(self, instance):
	# 	return instance.user.name

	# def staff_phone(self, instance):
	# 	return instance.user.phone

	def dcs(self,instance):
		allDcs=instance.dcs.all()
		myDcList=""
		for dc in allDcs:
			myDcList=myDcList+" :: "+dc.name
		return myDcList


class RetailerDeviceAdmin(admin.ModelAdmin):
	list_display=('id','retailer_name','retailer_phone','device_model', 'device_id')
	search_fields=['id', 'device_id']

	def retailer_name(self, instance):
		return instance.retailer.user.name

	def retailer_phone(self, instance):
		return instance.retailer.user.phone
	
	def device_model(self, instance):
		return instance.device.device_model
	
	def device_id(self, instance):
		return instance.device.device_id

# class RetailerShopAdmin(admin.ModelAdmin):
# 	list_display=('id','retailer_name','retailer_phone','dc_name','updated')
# 	search_fields=['id','shopName']

	# def retailer_name(self, instance):
	# 	return instance.retailer.user.name

	# def retailer_phone(self, instance):
	# 	return instance.retailer.user.phone

	# def dc_name(self, instance):
	# 	return instance.retailer.dc.name

# class StaffDeviceAdmin(admin.ModelAdmin):
# 	list_display=('deviceId','playerId','deviceModel','deviceManufacturer','staff_name','staff_phone','created')
# 	search_fields=['id','playerId',]

# 	def staff_name(self, instance):
# 		staff_name=""
# 		if instance.staff!=None:
# 			staff_name=instance.staff.name
# 		return staff_name

# 	def staff_phone(self, instance):
# 		staff_phone=""
# 		if instance.staff!=None:
# 			staff_phone=instance.staff.phone
# 		return staff_phone
		

# admin_site = HumusAdminSite(name='HumusVCManager')
	
admin.site.register(AddressType, AddressTypeAdmin)
admin.site.register(BasicUser, BasicUserAdmin)
admin.site.register(Addresses, AddressAdmin)
admin.site.register(Retailer, RetailerAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(RetailerDevice, RetailerDeviceAdmin)
admin.site.register(RetailerShop, RetailerShopAdmin)
admin.site.register(RetailerNotification)
admin.site.register(City)
admin.site.register(Device)
admin.site.register(RetailerCommodityRequests)
admin.site.register(NotificationType)

# admin_site.register(Distributor,DistributorAdmin)
# admin_site.register(Customer,CustomerAdmin)
# admin_site.register(StaffDevice,StaffDeviceAdmin)
# admin_site.register(Party)
# admin_site.register(PartyType)
# admin_site.register(PartyPayments)
# admin_site.register(RetailerDiscounts)
# admin_site.register(CommodityDiscount)
# admin_site.register(Banks)
# admin_site.register(StoreCustomer)
# admin_site.register(RetailStoreManager)
# admin_site.register(DistributionManager,DMAdmin)


