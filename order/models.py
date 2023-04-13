from datetime import datetime
from pytz import timezone

from django.utils.timezone import localtime

from django.db import models

from commodity.models import DcCommodity, DcCommodityBatch
from account.models import Retailer, Staff, DistributionCenterManager, RetailerShop
from office.models import DistributionCenter

ITEM_STATUS = (('New', 'New'), ('Out_Of_Stock', 'Out_Of_Stock'), ('Cancelled', 'Cancelled'),
               ('Awaiting_Confirmation', 'Awaiting_Confirmation'), ('Edited','Edited'),
               ('Partially_Cancelled', 'Partially_Cancelled'), ('Packed', 'Packed'),
               ('Delivery_Agent_Assigned', 'Delivery_Agent_Assigned'),
               ('Ready_For_Delivery', 'Ready_For_Delivery'),
               ('Delivery-In-Progress', 'Delivery-In-Progress'), ('Delivered', 'Delivered'),
               ('Partial_Delivery', 'Partial_Delivery'), ('Partial_Return', 'Partial_Return'),
               ('Return_Rejected', 'Return_Rejected'), ('Partial_Packed','Partial_Packed'),
               ('Return_Requests', 'Return_Requests'), ('Damage_Reported', 'Damage_Reported'),
               ('Damages_Rejected', 'Damages_Rejected'), ('Damages_Approved', 'Damages_Approved'),
               ('Returned', 'Returned'), ('DELETED', 'DELETED'))

ORDER_STATUS = (('New','New'),('Cancelled','Cancelled'),('Edited','Edited'),
            	('Partially_Cancelled','Partially_Cancelled'),('Packed','Packed'),
		    	('Packing_Started', 'Packing_Started'),
	         	('Delivery_Agent_Assigned','Delivery_Agent_Assigned'),
	         	('Ready_For_Delivery','Ready_For_Delivery'),
	          	('Delivery_In_Progress','Delivery_In_Progress'),
	          	('Delivered','Delivered'),('Partial_Delivery','Partial_Delivery'),
	          	('Partial_Packed','Partial_Packed'),('DELETED','DELETED'))

RETURN_ITEM_STATUS = (('New','New'),('Rejected','Rejected'),('Approved','Approved'))

DAMAGE_REPORT_ITEM_STATUS = (('New','New'),('Rejected','Rejected'),('Approved','Approved'))

OPERATION_MODE = (('B2B','B2B'),('B2C','B2C'))

class OrderItem(models.Model):
	commodity = models.ForeignKey(DcCommodity, null=False, on_delete=models.PROTECT)
	commodity_batch = models.ForeignKey(DcCommodityBatch, null=False, on_delete=models.PROTECT)
	quantity = models.FloatField(null=False)
	delivery_charge = models.FloatField(null=False, default=0.0)
	delivered_qty = models.FloatField(default=0.0)
	price = models.FloatField(null=False)
	sgst = models.FloatField(null=False, default=0.0)
	cgst = models.FloatField(null=False, default=0.0)
	status = models.CharField(max_length=100, default="New", choices=ITEM_STATUS)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	is_bulk_order = models.BooleanField(default=False)

	class Meta:
		verbose_name = u'B2B OrderItem'
		verbose_name_plural = u'B2B Order items'

	def __str__(self):
		return "   :product Name:  "+self.commodity.commodity.name + ' :quantity: ' + str(self.quantity)+ ' :price: '+str(self.price)

class Notes(models.Model):
	note = models.CharField(max_length=100, null=False, blank=False)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.id} {self.note}"

class ShippingVendor(models.Model):
	name = models.CharField(max_length=50, null=False, blank=False)
	is_active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
			return f"{self.id} {self.name}"

class Order(models.Model):
	order_items = models.ManyToManyField(OrderItem, related_name="order")
	retailer = models.ForeignKey(Retailer, null=False, on_delete=models.PROTECT)
	address = models.ForeignKey(RetailerShop, null=True, blank=True, on_delete=models.CASCADE)
	amount = models.FloatField(null=False)
	pending_amount = models.FloatField(null=False)
	notes = models.ManyToManyField(Notes)
	shipping_vendor = models.ForeignKey(ShippingVendor, null=True, blank=True, on_delete=models.CASCADE)
	dispatch_dc = models.ForeignKey(DistributionCenter, null=True, blank=True, on_delete=models.CASCADE)
	inv_url = models.CharField(max_length=600, null=True, blank=True)
	long_url = models.CharField(max_length=600, null=True, blank=True)
	updated = models.DateTimeField(auto_now=True)
	is_admin_verified = models.BooleanField(default=False)
	created = models.DateTimeField(default=datetime.now)
	delivery_incharge = models.ForeignKey(Staff, null=True, related_name="delivery_incharge", blank=True, on_delete=models.DO_NOTHING)
	packed_start_time = models.DateTimeField(null=True, blank=True)
	packed_end_time = models.DateTimeField(null=True, blank=True)
	shipped_time = models.DateTimeField(null=True, blank=True)
	delivery_time = models.DateTimeField(null=True, blank=True)
	status = models.CharField(max_length=100, default="New", choices=ORDER_STATUS)
	order_no = models.CharField(max_length=40, null=True, blank=True)
	manager_comments = models.CharField(max_length=2048, null=True, blank=True)
	staff_comments = models.CharField(max_length=2048, null=True, blank=True)
	retailer_comments = models.CharField(max_length=2048, null=True, blank=True)
	staff_rating = models.IntegerField(null=True, blank=True, default=5)
	retailer_rating = models.IntegerField(null=True, blank=True, default=5)
	is_staff_feed_back_provided = models.BooleanField(default=False)
	is_retailer_feed_back_provided = models.BooleanField(default=False)
	image_url = models.CharField(null=True, max_length=2048, blank=True)
	is_post_confirmation_required = models.BooleanField(default=False)

	@property
	def order_payments(self):
		return self.orderpayment_set.all()
		
	@property
	def converted_pack_start(self):
		# datetime_format = "%Y-%m-%dT%H:%M:%S+%H:%M"
		if self.packed_start_time:
			current_date_time = localtime(self.packed_end_time, timezone('Asia/Kolkata'))
			# date_split = current_date_time.split("+")[0]
			# date_datime = datetime.strptime(date_split, datetime_format)
			date = datetime.strftime(current_date_time.date(), "%d-%m-%Y")
			time = current_date_time.time()
			return f"{date} {time}"
	
	@property
	def converted_pack_end(self):
		# datetime_format = "%Y-%m-%dT%H:%M:%S+%H:%M"
		if self.packed_end_time:
			current_date_time = localtime(self.packed_end_time, timezone('Asia/Kolkata'))
			# date_split = current_date_time.split("+")[0]
			# date_datime = datetime.strptime(date_split, datetime_format)
			date = datetime.strftime(current_date_time.date(), "%d-%m-%Y")
			time = current_date_time.time()
			return f"{date} {time}"
		
	@property
	def converted_delivery_time(self):
		# datetime_format = "%Y-%m-%dT%H:%M:%S+%H:%M"
		if self.delivery_time:
			current_date_time = localtime(self.delivery_time, timezone('Asia/Kolkata'))
			# date_split = current_date_time.split("+")[0]
			# date_datime = datetime.strptime(date_split, datetime_format)
			date = datetime.strftime(current_date_time.date(), "%d-%m-%Y")
			time = current_date_time.time()
			return f"{date} {time}"

	@property
	def get_total_products(self):
		orders = self.order_items.all()
		total_products = 0
		for order_item in orders:
			if order_item.status != 'Out_Of_Stock':
				total_products += order_item.quantity
		return str(total_products)

	def save(self, *args, **kwargs):
		if self.created is None:
			self.created = datetime.datetime.now()
		super(Order, self).save(*args, **kwargs)
	
	class Meta:
		verbose_name = u'B2B Order'
		verbose_name_plural = u'B2B Orders'

	def __str__(self):
		return "   :Retailer Name:   "+self.retailer.user.name + ' :amount: ' + str(self.amount)+ ' :created: '+str(self.created)

class OrderItemReturnRequest(models.Model):
    order_item = models.ForeignKey(OrderItem, null=False, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, null=False, on_delete=models.PROTECT)
    returned_qty = models.FloatField(null=False, blank=False)
    return_reason = models.CharField(max_length=500, null=True)
    amount = models.FloatField(null=True)
    comments = models.CharField(max_length=2048, null=True, blank=True)
    image_url = models.CharField(null=True, max_length=2048, blank=True)
    status = models.CharField(max_length=100, default="New", choices=RETURN_ITEM_STATUS)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u'OrderItem Return'
        verbose_name_plural = u'OrderItem Returns'

    def __str__(self):
    	return "   :product Name:  "+self.order_item.commodity.commodity.name + ' :returned quantity: ' + str(self.returned_qty)+ ' :price: '+str(self.order_item.price)

PAYMENT_STATUS_CHOICES = (('INIT', 'INIT'), ('PROCESSING', 'PROCESSING'), ('SUCCESS', 'SUCCESS'),
						  ('FAILED', 'FAILED'), ('APPROVED', 'APPROVED'), ('APPROVAL_PENDING','APPROVAL PENDING'),
						  ('ORDER_FAILED_RETURN_TO_CUSTOMER','ORDER_FAILED_RETURN_TO_CUSTOMER'),
						  ('COMPLETED', 'COMPLETED'), ('ORDER_FAILED_REFUND', 'ORDER_FAILED_REFUND'),
						  ('PARTIAL_REFUND_GENERATED', 'PARTIAL_REFUND_GENERATED'),
						  ('REFUND_GENERATED', 'REFUND_GENERATED'), ('REFUND_REQUESTED', 'REFUND_REQUESTED'),
						  ('REFUND_REJECTED', 'REFUND_REJECTED'), ('DECLINED', 'DECLINED'))

class RetailerPayment(models.Model):
	retailer = models.ForeignKey(Retailer, on_delete=models.PROTECT)
	payment_mode = models.CharField(max_length=50, null=True, blank=True)
	is_online_payment = models.BooleanField(default=False)
	txn_id = models.CharField(null=False, max_length=100)
	amount = models.FloatField(null=False)
	is_verified_by_admin = models.BooleanField(default=False)
	product_info = models.CharField(null=False, max_length=100)
	payment_hash = models.CharField(null=True, max_length=1000)
	status = models.CharField(null=False, max_length=100, default='INIT', choices=PAYMENT_STATUS_CHOICES)
	google_pay_status = models.CharField(null=True, max_length=100, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = u'B2B Digital Payment'
		verbose_name_plural = u'B2B Digital Payments'

	def __str__(self):
		return f'retailer: {self.retailer.user.name} '+ 'amount: ' +str( self.amount)+ ' :created: '+str(self.created)
	
ORDER_PAYMENT_STATUS_CHOICES = (('NEW','NEW'),('ORDER_FAILED_REFUND','ORDER_FAILED_REFUND'),
								('REFUND_GENERATED','REFUND_GENERATED'),('OTP_GENERATED','OTP_GENERATED'),
								('OTP_VERIFIED','OTP_VERIFIED'),('ADMIN_VERIFIED','ADMIN_VERIFIED'),
								('COMPLETED','COMPLETED'))

PAYMENT_TYPES = (('DIGITAL_PAYMENT', 'DIGITAL_PAYMENT'), ('CREDIT_LIMIT', 'CREDIT_LIMIT'), ('POSTAL', 'POSTAL'))

class OrderPayment(models.Model):
	order = models.ForeignKey(Order, on_delete=models.PROTECT)
	retailer_payment = models.ForeignKey(RetailerPayment, on_delete=models.PROTECT, null=True, blank=True)
	payment_type = models.CharField(choices=PAYMENT_TYPES ,null=False, max_length=100, default='none')
	amount = models.FloatField(null=False)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	is_verified_by_admin = models.BooleanField(default=False)
	collected_by = models.ForeignKey(Staff,null=True, on_delete=models.DO_NOTHING, blank=True)
	status = models.CharField(null=False, max_length=100, default='NEW', choices=ORDER_PAYMENT_STATUS_CHOICES)

	def __str__(self):
		return f'retailer: {self.order.retailer.user.name} '+ ' :amount: ' +str(self.amount)+ ' :created: '+str(self.created)


REFUND_STATUS_CHOICES = (('NEW','NEW'), ('REJECTED','REJECTED'), ('COMPLETED','COMPLETED'),
						 ('APPROVED','APPROVED'))

class B2bRefundRequest(models.Model):
	retailer_payment = models.ForeignKey(RetailerPayment, on_delete=models.CASCADE, null=False, blank=True)
	amount = models.FloatField(null=False)
	status = models.CharField(null=False, max_length=100, default='NEW', choices=REFUND_STATUS_CHOICES)
	razor_pay_status = models.CharField(null=True, max_length=100, blank=True)
	refund_tnx_id = models.CharField(null=True, blank=True, max_length=50)
	comments = models.CharField(max_length=2048,null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	approval_otp = models.CharField(null=True, blank=True, max_length=10)
	otp_creation_time = models.DateTimeField(null=True, blank=True)

	class Meta:
		verbose_name = u'retailerRefundRequest'
		verbose_name_plural = u'retailerRefundRequest'

	def __str__(self):
		return "   :Retailer Name:   "+self.retailer_payment.retailer.user.name + ' :amount: ' + str(self.amount)+' :payment_id: '+str(self.retailer_payment.id)

class OrderItemHistory(models.Model):
	order_item = models.ForeignKey(OrderItem, on_delete=models.PROTECT)
	updated_status = models.CharField(max_length=100, default="New", choices=ORDER_STATUS)
	log = models.CharField(max_length=1024)

	class Meta:
		verbose_name = u'Order Item History'
		verbose_name_plural = u'Order Item History'

	def __str__(self):
		return "   :Order Item  "+self.order_item.id

class OrderHistory(models.Model):
	order = models.ForeignKey(OrderItem, on_delete=models.PROTECT)
	updated_status = models.CharField(max_length=100, default="New", choices=ORDER_STATUS)
	log = models.CharField(max_length=1024)

	class Meta:
		verbose_name = u'Order History'
		verbose_name_plural = u'Order  History'

	def __str__(self):
		return "   :Order Item  "+self.order.id

TRANSFER_REQUEST_STATUS = (('Requested', 'Requested'), ('Partial_Fulfilled', 'Partial_Fulfilled'),
						   ('Fulfilled', 'Fulfilled'))

#Required Change According To Transfre Stocks From One DC to another
class StockTransferRequest(models.Model):
	dc_manager = models.ForeignKey(DistributionCenterManager, null=False, on_delete=models.PROTECT)
	requested_from = models.ForeignKey(DistributionCenter, null=False, on_delete=models.CASCADE)
	dc_commodity = models.ForeignKey(DcCommodity, null=False, on_delete=models.CASCADE)
	required_qty = models.FloatField(null=False)
	shortage_qty = models.FloatField(null=True, blank=True)
	is_active = models.BooleanField(default=True)
	status = models.CharField(null=False, max_length=100, default='Requested', choices=TRANSFER_REQUEST_STATUS)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	# def __str__(self):
	# 	return "Commodity: "+ self.dc_ommodity.commodity.name + "RetailStore:   "+ self.retailStore.shopName


# TRANSFER_FULFILMENT_STATUS = (('Transferred', 'Transferred'), ('Received', 'Received'))

#Required Change Accordingly
# class StockTransferFulfilment(models.Model):
# 	fulfilled_store_manager = models.ForeignKey(DistributionStoreManager, null=False, on_delete="PROTECT")
# 	transfer_request = models.ForeignKey(StockTransferRequest, null=False, on_delete="CASCADE")
# 	fulfilled_store = models.ForeignKey(RetailStore, null=False, on_delete="CASCADE")
# 	fulfilled_qty = models.FloatField(null=False)
# 	is_active = models.BooleanField(default=True)
# 	status = models.CharField(null=False,max_length=100, default='Transferred', choices=TRANSFER_FULFILMENT_STATUS)
# 	updated = models.DateTimeField(auto_now=True)
# 	created = models.DateTimeField(auto_now_add=True)

# 	def __str__(self):
# 		return "Commodity: "+ self.transferRequest.storeCommodity.commodity.name + "RetailStore:   "+ self.fulfilledStore.shopName
