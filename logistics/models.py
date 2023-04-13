from django.db import models

from account.models import Staff, Retailer
from office.models import DistributionCenter

class RouteLists(models.Model):
	name = models.CharField(null=False, max_length=100)
	dc = models.ForeignKey(DistributionCenter, null=False, on_delete=models.SET_DEFAULT, default=1)
	is_active = models.BooleanField(default=True)
	#Change of feature to have multiple delivery staff per route
	delivery_staff = models.ManyToManyField(Staff)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return str(self.name)

class RetailerRouteMapping(models.Model):
	retailer = models.OneToOneField(Retailer, null=False, on_delete=models.CASCADE)
	route = models.ForeignKey(RouteLists, null=False, on_delete=models.CASCADE)
	en_route_no = models.IntegerField(default=9999, null=False, blank=False)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __unicode_(self):
		return str(self.retailer.name)+" ::  "+str(self.enRouteNo)
