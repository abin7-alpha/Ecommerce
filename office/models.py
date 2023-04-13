from django.db import models

from geoposition.fields import GeopositionField

class DistributionCenter(models.Model):
	name = models.CharField(null=False, max_length=150)
	city = models.CharField(null=False, max_length=100)
	pincode = models.CharField(null=True, max_length=10, blank=True)
	position = GeopositionField()
	is_active = models.BooleanField(default=True)
	is_primary_dC = models.BooleanField(default=False)
	samed_day_delivery_last_order_time = models.TimeField(null=True, blank=False)
	minimum_b2b_day_order_amount = models.FloatField(null=True, blank=True, default=0.0)

	def __str__(self):
		return str(self.name)+" "+str(self.city)

class City(models.Model):
	name = models.CharField(null=False, max_length=200)
	city_bounds_upper = GeopositionField(null=True)
	city_bounds_lower = GeopositionField(null=True)
	city_center = GeopositionField(null=True)
	is_active = models.BooleanField(default=True)
	def __str__(self):
		return str(self.name)

class Area(models.Model):
	name = models.CharField(null=False, max_length=150)
	city = models.CharField(null=False, max_length=100)
	pincode = models.CharField(null=True, max_length=10, blank=True)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return str(self.name)+" : "+str(self.city)

APP_NAMES= (('Captains_App', 'Captains_App'), ('Retailer_App', 'Retailer_App'), 
            ('Retailer_Web', 'Retailer_Web'), ('Retailer_Mail', 'Retailer_Mail'))

class NotificationRecords(models.Model):
	title = models.CharField(null=False,max_length=150)
	subtitle = models.CharField(null=True,max_length=150)
	content = models.CharField(null=True,max_length=1024)	
	image_url = models.CharField(max_length=650, null=True,blank=True)
	app_name = models.CharField(max_length=100,choices=APP_NAMES,null=True)
	is_in_kannada = models.BooleanField(null=False,default=False)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.title)+ ": appName : "+str(self.appName)

#Required Run Cron Job end Of Day updateed details for DC
class DcDailyTransactions(models.Model):
	distribution_center = models.ForeignKey(DistributionCenter, null=False, on_delete=models.PROTECT)
	total_num_orders = models.FloatField(null=True, blank=True, default=0.0)
	total_revenue = models.FloatField(null=True, blank=True, default=0.0)
	created = models.DateTimeField(auto_now_add=True)
	date = models.DateTimeField(auto_now_add=False)

	def __str__(self):
		return str(self.distribution_center.name)+ ": Total Revenue : "+str(self.total_revenue)
	