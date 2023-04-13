from django.contrib import admin

from order.models import OrderItem, Order, OrderHistory, OrderItemReturnRequest, OrderPayment, Notes, ShippingVendor
from order.models import RetailerPayment, B2bRefundRequest, OrderItemHistory, StockTransferRequest


class OrderAdmin(admin.ModelAdmin):
	"""docstring for ClassName"""
	list_display=('id', 'retailer_name', 'order_no', 'amount', 'pending_amount', 'created', 'updated', 'status')
	search_fields=['id', 'order_no', 'amount', 'status']

	def retailer_name(self, instance):
		return instance.retailer.user.name


class OrderItemAdmin(admin.ModelAdmin):
	"""docstring for ClassName"""
	list_display=('id', 'commodity_name', 'created', 'updated')
	search_fields=['id', 'price']

	def orderNo(self, instance):
		orders=Order.objects.filter(orderItems__in=[instance]).distinct().all()
		if len(orders)>0:
			return orders[0].orderNo
		return "No order for order item: "+str(instance.id)

	def commodity_name(self, instance):
		return instance.commodity.commodity.name
	
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderHistory)
admin.site.register(OrderItemReturnRequest)
admin.site.register(OrderPayment)
admin.site.register(RetailerPayment)
admin.site.register(B2bRefundRequest)
admin.site.register(OrderItemHistory)
admin.site.register(StockTransferRequest)
admin.site.register(Notes)
admin.site.register(ShippingVendor)
