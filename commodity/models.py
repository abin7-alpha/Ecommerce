from django.db import models
from django_boto.s3.storage import S3Storage

from janaushadi import settings

from office.models import DistributionCenter

from imageControl.models import Image

from datetime import datetime
from pytz import timezone

s3 = S3Storage(replace=True)

class CommodityCategory(models.Model):
	name = models.CharField(null=False, max_length=200, unique=True)
	is_active = models.BooleanField(default=True)
	image_url = models.CharField(null=True, max_length=2048, blank=True)
	
	def __str__(self):
		return str(self.name)+" : Is Active :  "+str(self.is_active) + str(self.id)

class CommodityGroup(models.Model):
	name = models.CharField(null=False, max_length=200,unique=True)
	is_active = models.BooleanField(default=True)
	image_url = models.CharField(null=True, max_length=2048, blank=True)
	
	def __str__(self):
		return str(self.name)+" : Is Active :  "+str(self.is_active) + str(self.id)

class DrugManufacturer(models.Model):
	name = models.CharField(null=False, max_length=200, unique=True)
	is_active = models.BooleanField(default=True)
	
	def __str__(self):
		return str(self.name)+" : Is Active :  "+str(self.is_active)

class CommodityMeasuringUnits(models.Model):
	name=models.CharField(null=False,max_length=200)
	is_active=models.BooleanField(default=True)

	def __str__(self):
		return str(self.name)

class Commodity(models.Model):
	measuring_unit=models.ForeignKey(CommodityMeasuringUnits, null=False, default="10's", on_delete=models.PROTECT)
	commodity_category = models.ForeignKey(CommodityCategory, null=False, on_delete=models.PROTECT)
	commodity_group = models.ForeignKey(CommodityGroup, null=False, on_delete=models.PROTECT)
	drug_manufacturer = models.ForeignKey(DrugManufacturer, null=False, on_delete=models.PROTECT)
	name = models.CharField(null=False, max_length=200)
	salt_name = models.CharField(null=True, blank=True, max_length=200)
	mm_code = models.CharField(null=False, max_length=200, unique=True)
	hsncode = models.CharField(null=False, max_length=200)
	searchkey = models.CharField(null=True, blank=True, max_length=200)
	mtm_name = models.CharField(null=False, max_length=200)
	description = models.CharField(null=True,max_length=1024)
	uom_code = models.CharField(null=True, max_length=200)
	mcm_name = models.CharField(null=True, max_length=200)
	image=models.ImageField(upload_to='media/commodity_image/', null=True, blank=True,max_length=None)
	image_url = models.CharField(null=True, max_length=2048, blank=True)
	images = models.ManyToManyField(Image, blank=True)
	gst = models.FloatField(null=False, default=0)
	igst = models.FloatField(null=False, default=0)
	is_active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	priority = models.FloatField(null=True, default=0)

	def __str__(self):
		return str(self.name)

current_date_time = timezone('Asia/Kolkata').localize(datetime.now())

class DcCommodity(models.Model):
	distribution_center = models.ForeignKey(DistributionCenter, null=False, on_delete=models.PROTECT, default=1)
	commodity = models.ForeignKey(Commodity, null=False, on_delete=models.PROTECT,  limit_choices_to = {'is_active': True})
	available_quantity = models.FloatField(null=True)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	min_available_qty = models.FloatField(null=True, default=1.0)
	max_available_qty = models.FloatField(null=True, default=available_quantity)
	max_qty_allowed_per_order = models.FloatField(null=True, default=settings.MAX_QUANTITY_ALLOWED_PER_ORDER)
	minimum_order_quantity = models.FloatField(default=1.0, blank=False,null=True)
	created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	last_availability_notified = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, null=True, blank=True)
	# is_under_janaushadi = models.BooleanField(default=False)
	is_janaushadi = models.BooleanField(default=False)


	def __str__(self):
		return str(self.commodity.name)
	
	@property
	def commodity_batches(self):
		return self.dccommoditybatch_set.all()

class DcCommodityBatch(models.Model):
	batch_id = models.CharField(max_length=100, null=True, blank=True)
	dc_commodity = models.ForeignKey(DcCommodity, null=False, on_delete=models.PROTECT)
	mrp = models.FloatField(null=True)
	price = models.FloatField(null=True)
	minimum_order_quantity = models.FloatField(default=1.0, blank=False, null=True)
	expiry_date = models.DateField(null=False)
	is_active = models.BooleanField(default=True)
	available_quantity = models.FloatField(null=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('expiry_date',)

	def __str__(self):
		return str(self.price)

QTY_CHANGE_TYPE=(('Increment','Increment'),('Decrement','Decrement'))

class DcCommodityBatchLog(models.Model):
	batch = models.ForeignKey(DcCommodityBatch, null=False, on_delete=models.PROTECT)
	# staff = models.ForeignKey()
	qty_change = models.FloatField(null=True)
	change_type = models.CharField(null=False, max_length=100, choices=QTY_CHANGE_TYPE)
	available_quantity = models.FloatField(null=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.id)

INDENTS_STATUS = (('Requested', 'Requested'), ('Shortage', 'Shortage'), ('Fulfilled', 'Fulfilled'))

class DistributionStoreIndent(models.Model):
	dc = models.ForeignKey(DistributionCenter, null=False, on_delete=models.CASCADE)
	dc_commodity = models.ForeignKey(DcCommodity, null=False, on_delete=models.CASCADE)
	requested_qty = models.FloatField(null=False)
	shortage_qty = models.FloatField(null=True, blank=True)
	fulfilled_qty = models.FloatField(null=True, blank=True)
	is_active = models.BooleanField(default=True)
	status = models.CharField(null=False, max_length=100, default='Requested', choices=INDENTS_STATUS)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.id) + "commodity:"+ str(f"   {self.dc.name}") + "CC:   "+ self.dc_commodity.commodity.name

class DistributionStoreIndentHistory(models.Model):
	store_indent = models.ForeignKey(DistributionStoreIndent, null=False, on_delete=models.CASCADE)
	indent_log = models.CharField(max_length=2048, null=True, blank=True)
	qty_change = models.FloatField(null=True, blank=True)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "indent_log: "+ self.indent_log
	